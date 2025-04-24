from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.utils.timezone import now

from core.forms import CustomLoginForm
from core.models import Felhasznalo


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



