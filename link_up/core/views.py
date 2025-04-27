from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils.timezone import now
from .forms import CustomRegisterForm
from core.forms import CustomLoginForm
from django.db import connection
from django.http import HttpResponse

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        user.utolso_bejelentkezes = now()
        user.save(update_fields=['utolso_bejelentkezes'])
        return super().form_valid(form)

def index(request):
    return render(request, 'index.html')


@login_required
def user_info(request):
    return render(request, 'user_info.html', {
        'time': datetime.now(),
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


