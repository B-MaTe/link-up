import datetime

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.decorators.http import require_POST

from .dto import SearchUser, Page
from .forms import CustomRegisterForm
from core.forms import CustomLoginForm
from django.db import connection
from django.http import HttpResponse

from .models import Felhasznalo, Bejegyzes, FelhasznaloKapcsolat, Csoport, FelhasznaloCsoport, Uzenet
from .service import bejegyzes_service, image_service
from core.enums import BejegyzesResponse, ImageCreationResponse, KapcsolatStatus, from_string, UzenetResponse
from .service.bejegyzes_service import add_komment


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
    friends = []

    if request.user.is_authenticated:
        all = FelhasznaloKapcsolat.objects.filter(
            Q(Q(jelolo=request.user) | Q(jelolt=request.user)) & Q(statusz=KapcsolatStatus.ACCEPTED.name.lower()))

        for kapcsolat in all:
            if kapcsolat.jelolo == request.user:
                friends.append(
                    SearchUser(kapcsolat.jelolt.id, kapcsolat.jelolt.felhasznalonev, kapcsolat.jelolt.profil_kep))
            else:
                friends.append(
                    SearchUser(kapcsolat.jelolo.id, kapcsolat.jelolo.felhasznalonev, kapcsolat.jelolo.profil_kep))

    if request.method == 'GET':
        page: Page = Page(1, 5, 1, False, False)
        page.current = int(request.GET.get('page', 1))
        count_pages = Bejegyzes.objects.all().count()
        page.total_pages = count_pages // page.size
        page.has_next = count_pages > page.current * page.size
        page.has_previous = page.current > 1
        page.page_range = range(1, page.total_pages + 2)
        page.next = min(page.current + 1, page.total_pages + 1)
        page.previous = max(page.current - 1, 1)
        posts = Bejegyzes.objects.all().prefetch_related('kommentek').order_by('-id')[(page.current - 1) * page.size:(page.current + 1) * page.size]

        return render(request, 'index.html', {'posts': posts, 'page': page, 'friends': friends})

    if request.method == 'POST':
        if "add-post" in request.POST:
            text = request.POST.get('post')
            img = request.FILES.get('image')

            data['post'] = text
            data['image'] = img

            result = bejegyzes_service.create_bejegyzes(request, text, img)

            if result == BejegyzesResponse.PROFANITY:
                return render(request, 'index.html', {'profanity': True, 'data': data, 'friends': friends})

            if result == BejegyzesResponse.FILE_FORMAT_ERROR:
                return render(request, 'index.html', {'file_format_error': True, 'data': data, 'friends': friends})

            if result == BejegyzesResponse.ERROR:
                return render(request, 'index.html', {'error': True, 'data': data, 'friends': friends})

            return redirect('index')

    return render(request, 'index.html', {'data': data, 'friends': friends})


def add_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        comment = request.POST.get('comment')

        response = add_komment(Bejegyzes.objects.get(id=post_id), request.user, comment)

        if response == UzenetResponse.PROFANITY:
            return HttpResponse({'profanity': True})

        if response == UzenetResponse.ERROR:
            return HttpResponse({'error': True})

        return HttpResponse({'success': True})

@require_POST
def search_users(request):
    query = request.POST.get('query')
    if not query or len(query.strip()) < 1:
        return HttpResponse('')

    users = Felhasznalo.objects.filter(felhasznalonev__icontains=query)[:15]

    prepared_users = []
    for user in users:
        prepared_users.append(SearchUser(user.id, user.felhasznalonev, user.profil_kep))

    return render(request, 'partial/user_list.html', {'users': prepared_users})


@login_required
def user_info(request, user_id=None):
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
        kapcsolat = FelhasznaloKapcsolat.objects.filter(
            Q(jelolo=from_user, jelolt=to_user) | Q(jelolo=to_user, jelolt=from_user)).first()
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
                kapcsolat = FelhasznaloKapcsolat.objects.get_or_create(jelolo=from_user, jelolt=to_user,
                                                                       statusz=KapcsolatStatus.PENDING.name.lower())
                if kapcsolat:
                    status = from_string(kapcsolat[0].statusz)
                    added = True

            return render(request, 'user_info.html', {
                'user': user,
                'readonly': user != request.user,
                'added': added,
                'status': status.name
            })
        elif "change_username" in request.POST:
            if not same_user:
                return redirect('user_info', user_id=user.id)

            new_username = request.POST.get('new_username')
            existing_user = Felhasznalo.objects.filter(felhasznalonev=new_username).first()
            if existing_user:
                return render(request, 'user_info.html', {
                    'user': user,
                    'readonly': user != request.user,
                    'user_exists': True
                })

            user.felhasznalonev = new_username
            user.save(update_fields=['felhasznalonev'])
            return render(request, 'user_info.html', {
                'user': user,
                'readonly': user != request.user,
                'user_exists': False,
                'username_updated': True
            })
        elif "delete_profile" in request.POST:
            if not same_user:
                return redirect('user_info', user_id=user.id)
            user.delete()
            return redirect('index')

    return render(request, 'user_info.html', {
        'user': user,
        'readonly': user != request.user,
        'status': status.name,
    })


def connections(request):
    message = None

    if request.method == 'POST':
        affected_id = request.POST.get('affected_id')
        action = request.POST.get('action')
        kapcsolat = FelhasznaloKapcsolat.objects.get(jelolo_id=affected_id, jelolt_id=request.user.id)
        if "accept" == action:
            kapcsolat.statusz = KapcsolatStatus.ACCEPTED.name.lower()
            kapcsolat.save(update_fields=['statusz'])
            message = "Jelölés sikeresen elfogadva! Mostmár ismerősök vagytok"
        elif "reject" == action:
            kapcsolat.statusz = KapcsolatStatus.REJECTED.name.lower()
            kapcsolat.save(update_fields=['statusz'])
            message = "Jelölés sikeresen elutasítva!"

    pending_from_user = FelhasznaloKapcsolat.objects.filter(jelolo=request.user,
                                                            statusz=KapcsolatStatus.PENDING.name.lower())
    pending_to_user = FelhasznaloKapcsolat.objects.filter(jelolt=request.user,
                                                          statusz=KapcsolatStatus.PENDING.name.lower())
    rejected_from_user = FelhasznaloKapcsolat.objects.filter(jelolo=request.user,
                                                             statusz=KapcsolatStatus.REJECTED.name.lower())
    rejected_to_user = FelhasznaloKapcsolat.objects.filter(jelolt=request.user,
                                                           statusz=KapcsolatStatus.REJECTED.name.lower())

    return render(request, 'connections.html', {
        'pending_from_user': pending_from_user,
        'pending_to_user': pending_to_user,
        'rejected_from_user': rejected_from_user,
        'rejected_to_user': rejected_to_user,
        'message': message
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


def kommentek_for_bejegyzes(request):
    bejegyzes_id = request.GET.get('bejegyzes_id')
    bejegyzes = Bejegyzes.objects.get(id=bejegyzes_id)
    return render(request, 'partial/comments.html', {'comments': bejegyzes.kommentek.all().order_by('-id')})

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
    csoportok = Csoport.objects.filter()
    sajat_csoportok = FelhasznaloCsoport.objects.filter(Q(felhasznalo_id=request.user.id))
    felhasznalo_name = request.user.felhasznalonev
    ismerosok = FelhasznaloKapcsolat.objects.filter(
        Q(Q(jelolo=request.user) | Q(jelolt=request.user)) & Q(statusz=KapcsolatStatus.ACCEPTED.name.lower()))
    ismeros_id_list = []
    sajat_csoportok_id_list = []
    active_group = None
    group_name = None
    group_uzenetek = []
    jelenlegi_csoport_id = None

    if request.method == 'POST':
        if "addGroup" in request.POST:
            csoport_nev = request.POST.get("gname")
            tagok_id = request.POST.getlist("tagok")
            egyedi_tagok_id = list(set(tagok_id))
            egyedi_tagok_id.append(str(request.user.id))
            uj_csoport = Csoport.objects.create(
                csoport_nev=csoport_nev,
                letrehozas_ido=datetime.datetime.now(),
                felhasznalo=request.user,
                privat_beszelgetes=False
            )

            FelhasznaloCsoport.objects.create(
                csoport=uj_csoport,
                felhasznalo=request.user
            )

            for tag_id in tagok_id:
                FelhasznaloCsoport.objects.create(
                    csoport=uj_csoport,
                    felhasznalo=Felhasznalo.objects.get(pk=tag_id),
                )

            return redirect('csoportok')

        elif "removeGroup" in request.POST:
            torlendo_csoport_id = request.POST.get("csoport-id")
            Csoport.objects.filter(pk=torlendo_csoport_id).delete()

        elif "guzenet" in request.POST:
            print(f"POST adatok: {request.POST}")

            gtext = request.POST.get("gtext")
            kuldo_id = request.POST.get("kuldo-id")
            csoport_id = request.POST.get("csoport-id")
            csoport = Csoport.objects.get(pk=csoport_id)
            active_group = csoport.id
            group_name = csoport.csoport_nev
            group_uzenetek = Uzenet.objects.filter(csoport=csoport).order_by('kuldesi_ido')
            jelenlegi_csoport_id = csoport.id

            Uzenet.objects.create(
                felhasznalo=Felhasznalo.objects.get(pk=kuldo_id),
                csoport=csoport,
                kuldesi_ido=datetime.datetime.now(),
                tartalom=gtext,
            )
        elif "open_csoport" in request.POST:
            csoport_id = request.POST.get("csoport_id")
            csoport = Csoport.objects.get(pk=csoport_id)
            group_uzenetek = Uzenet.objects.filter(csoport=csoport).order_by('kuldesi_ido')
            jelenlegi_csoport_id = csoport_id
            group_name = csoport.csoport_nev

    for kapcsolat in ismerosok:
        if kapcsolat.jelolo.id != request.user.id:
            ismeros_id_list.append(kapcsolat.jelolo.id)
        if kapcsolat.jelolt.id != request.user.id:
            ismeros_id_list.append(kapcsolat.jelolt.id)

    ismeros_id_list = list(set(ismeros_id_list))

    ismerosok = Felhasznalo.objects.filter(id__in=ismeros_id_list)

    for csoport in sajat_csoportok:
        for csopi in csoportok:
            if csopi.id == csoport.csoport_id:
                sajat_csoportok_id_list.append(csopi.id)

    sajat_csoportok_id_list = list(set(sajat_csoportok_id_list))
    csoportok = Csoport.objects.filter(id__in=sajat_csoportok_id_list)

    return render(request, 'groups.html', {
        'felhasznalo_name': felhasznalo_name,
        'ismerosok': ismerosok,
        'csoportok': csoportok,
        'active_chat': active_group,
        'group_name': group_name,
        'group_uzenetek': group_uzenetek,
        'jelenlegi_csoport_id': jelenlegi_csoport_id,
        'jelenlegi_kuldo_id': request.user.id
    })
