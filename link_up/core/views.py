from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.decorators.http import require_POST

from .dto import SearchUser, Page
from .forms import CustomRegisterForm
from core.forms import CustomLoginForm
from django.db import connection
from django.http import HttpResponse

from .models import Felhasznalo, Bejegyzes, FelhasznaloKapcsolat, Csoport, FelhasznaloCsoport
from .service import bejegyzes_service, image_service
from core.enums import BejegyzesResponse, ImageCreationResponse, KapcsolatStatus, from_string


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        user.utolso_bejelentkezes = now()
        user.save(update_fields=['utolso_bejelentkezes'])
        return super().form_valid(form)

def index(request):
    data = {}

    if request.method == 'GET':
        page: Page = Page(1, 5, 1, False, False)
        page.current = int(request.GET.get('page', 1))
        count_pages = Bejegyzes.objects.all().count()
        page.total_pages = count_pages // page.size
        page.has_next = count_pages > page.current * page.size
        page.has_previous = page.current > 0
        page.page_range = range(1, page.total_pages)
        posts = Bejegyzes.objects.all().order_by('-id')[page.current * page.size:(page.current + 1) * page.size]

        return render(request, 'index.html', {'posts': posts, 'page': page})

    if request.method == 'POST':
        if "add-post" in request.POST:
            text = request.POST.get('post')
            img = request.FILES.get('image')

            data['post'] = text
            data['image'] = img

            result = bejegyzes_service.create_bejegyzes(request, text, img)

            if result == BejegyzesResponse.PROFANITY:
                return render(request, 'index.html', {'profanity': True, 'data': data})

            if result == BejegyzesResponse.FILE_FORMAT_ERROR:
                return render(request, 'index.html', {'file_format_error': True, 'data': data})

            if result == BejegyzesResponse.ERROR:
                return render(request, 'index.html', {'error': True, 'data': data})

            return redirect('index')

    return render(request, 'index.html')


@require_POST
def search_users(request):
    query = request.POST.get('query')
    if not query or len(query.strip()) < 1:
        return HttpResponse('')

    users = Felhasznalo.objects.filter(felhasznalonev__icontains=query)[:5]

    prepared_users = []
    for user in users:
        prepared_users.append(SearchUser(user.id, user.felhasznalonev, user.profil_kep))

    return render(request, 'partial/user_list.html', {'users': prepared_users})


@login_required
def user_info(request, user_id = None):
    if user_id:
        user = Felhasznalo.objects.get(id=user_id)

        if not user:
            return redirect('index')
    else:
        user = request.user

    same_user = user.id == request.user.id

    status = KapcsolatStatus.NONE

    if not same_user:
        from_user = request.user
        to_user = Felhasznalo.objects.get(id=user.id)
        kapcsolat = FelhasznaloKapcsolat.objects.filter(jelolo=from_user, jelolt=to_user).first()
        if kapcsolat:
            status = from_string(kapcsolat.statusz)

    if request.method == 'POST':
        if "change-profile-pic" in request.POST:
            if not same_user:
                return redirect('user_info', user_id=user.id)

            img = request.FILES.get('image')
            file_format_error = False
            error = False
            success = False

            if img:
                response, file_name = image_service.create_image(img, "profile")
                if response == ImageCreationResponse.NOT_SUPPORTED_FILE_FORMAT:
                    file_format_error = True
                elif response == ImageCreationResponse.ERROR:
                    error = True
                elif response == ImageCreationResponse.SUCCESS:
                    user.profil_kep = file_name
                    user.save(update_fields=['profil_kep'])
                    success = True

            return render(request, 'user_info.html', {
                'user': user,
                'readonly': user != request.user,
                'file_format_error': file_format_error,
                'error': error,
                'success': success
            })
        elif "add_user" in request.POST:
            added = False

            if not same_user:
                from_user = request.user
                to_user = Felhasznalo.objects.get(id=user.id)
                kapcsolat = FelhasznaloKapcsolat.objects.get_or_create(jelolo=from_user, jelolt=to_user, statusz=KapcsolatStatus.PENDING.name.lower())
                if kapcsolat:
                    status = from_string(kapcsolat[0].statusz)
                    added = True


            return render(request, 'user_info.html', {
                'user': user,
                'readonly': user != request.user,
                'added': added,
                'status': status.name
            })

    return render(request, 'user_info.html', {
        'user': user,
        'readonly': user != request.user,
        'status': status.name,
    })

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            return redirect('index')
    else:
        form = CustomRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM dual")
            db_status = cursor.fetchone()
        if db_status and db_status[0] == 1:
            status = "Az adatbázis sikeresen kapcsolódott."
        else:
            status = "Sikertelen adatbázis kapcsolodás."
    except Exception as e:
        status = f"Adatbázis hiba: {str(e)}"

    html_content = f"""
    <html>
    <head><title>Health Check</title></head>
    <body>
        <h1>Health Check</h1>
        <p>{status}</p>
    </body>
    </html>
    """

    return HttpResponse(html_content)

def csoportok_view(request):
    # csoportok = Csoport.objects.all().order_by('-letrehozas_ido')  # Legújabb csoportok elöl
    # return render(request, 'groups.html', {'csoportok': csoportok})
    felhasznalo_name = request.user.felhasznalonev
    felhasznalok = Felhasznalo.objects.all()
    return render(request, 'groups.html', {
        'felhasznalo_name': felhasznalo_name,
        'felhasznalok': felhasznalok,
    })
