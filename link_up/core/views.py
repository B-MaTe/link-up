from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.decorators.http import require_POST

from .dto import SearchUser
from .forms import CustomRegisterForm
from core.forms import CustomLoginForm
from django.db import connection
from django.http import HttpResponse

from .models import Felhasznalo, Bejegyzes
from .service import bejegyzes_service


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
        posts = Bejegyzes.objects.all().order_by('-id')[:10]

        return render(request, 'index.html', {'posts': posts})

    if request.method == 'POST':
        if "add-post" in request.POST:
            text = request.POST.get('post')
            img = request.FILES.get('image')

            data['post'] = text
            data['image'] = img

            result = bejegyzes_service.create_bejegyzes(request, text, img)

            if result == bejegyzes_service.BejegyzesResponse.PROFANITY:
                return render(request, 'index.html', {'profanity': True, 'data': data})

            if result == bejegyzes_service.BejegyzesResponse.ERROR:
                return render(request, 'index.html', {'error': True, 'data': data})

            return redirect('index')

    return render(request, 'index.html')


@require_POST
def search_users(request):
    query = request.POST.get('query')
    if not query or len(query.strip()) < 3:
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

    return render(request, 'user_info.html', {
        'time': datetime.now(),
        'user': user,
        'readonly': user != request.user
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


