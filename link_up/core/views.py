import os
import uuid
from datetime import datetime, timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.utils.timezone import now

from core.forms import CustomLoginForm
from core.models import Felhasznalo, Bejegyzes, Csoport, Komment, Uzenet
from link_up import settings


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

#admin views
def bejegyzes(request):
    if request.method == 'POST':

        felhasznalo_id = request.POST.get('felhasznalo')
        feltoltott_kep = request.FILES.get('feltoltott_kep')
        letrehozasi_ido = request.POST.get('letrehozasi_ido')
        tartalom = request.POST.get('tartalom')

        if felhasznalo_id:
            felhasznalo = Felhasznalo.objects.get(id=felhasznalo_id)
        else:
            felhasznalo = None


        if letrehozasi_ido:
            letrehozasi_ido = datetime.strptime(letrehozasi_ido, "%Y-%m-%dT%H:%M")
        else:
            letrehozasi_ido = None

        if feltoltott_kep:
            kep_uuid = str(uuid.uuid4())
            kiterjesztes = os.path.splitext(feltoltott_kep.name)[1]
            uj_fajlnev = f"{kep_uuid}{kiterjesztes}"
            cel_utvonal = os.path.join('static', 'img', uj_fajlnev)

            file_content = ContentFile(feltoltott_kep.read())
            full_path = os.path.join(settings.BASE_DIR, "core", cel_utvonal)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'wb') as destination:
                destination.write(file_content.read())

        Bejegyzes.objects.create(
            felhasznalo=felhasznalo,
            feltoltott_kep=uj_fajlnev,
            letrehozasi_ido=letrehozasi_ido,
            tartalom=tartalom
        )

        return redirect('index')

    return render(request,"admin/bejegyzes.html", {
        'felhasznalok': Felhasznalo.objects.all(),
    })

def csoport(request):
    if request.method == 'POST':
        felhasznalo_id = request.POST.get('felhasznalo')
        letrehozas_ido = request.POST.get('letrehozas_ido')

        felhasznalo = None
        if felhasznalo_id:
            felhasznalo = Felhasznalo.objects.get(id=felhasznalo_id)

        if letrehozas_ido:
            letrehozas_ido = datetime.strptime(letrehozas_ido, "%Y-%m-%dT%H:%M")
        else:
            letrehozas_ido = None

        Csoport.objects.create(
            felhasznalo=felhasznalo,
            letrehozas_ido=letrehozas_ido
        )

        return redirect('index')

    felhasznalok = Felhasznalo.objects.all()
    return render(request, 'admin/csoport.html', {'felhasznalok': felhasznalok})

def komment(request):
    if request.method == 'POST':
        felhasznalo_id = request.POST.get('felhasznalo')
        bejegyzes_id = request.POST.get('bejegyzes_id')
        feltoltesi_ido = request.POST.get('feltoltesi_ido')
        tartalom = request.POST.get('tartalom')

        felhasznalo = Felhasznalo.objects.get(id=felhasznalo_id)
        komment_bejegyzes = Bejegyzes.objects.get(id=bejegyzes_id)

        if feltoltesi_ido:
            feltoltesi_ido = datetime.strptime(feltoltesi_ido, "%Y-%m-%dT%H:%M")

        uj_komment = Komment(
            felhasznalo=felhasznalo,
            bejegyzes=komment_bejegyzes,
            feltoltesi_ido=feltoltesi_ido,
            tartalom=tartalom
        )
        uj_komment.save()

        return redirect('index')

    else:

        bejegyzesek = Bejegyzes.objects.all()
        felhasznalok = Felhasznalo.objects.all()
        return render(request, 'admin/komment.html', {'bejegyzesek': bejegyzesek, 'felhasznalok': felhasznalok})


def uzenet(request):
    if request.method == 'POST':
        felhasznalo_id = request.POST.get('felhasznalo')
        csoport_id = request.POST.get('csoport')
        kuldesi_ido = request.POST.get('kuldesi_ido')
        tartalom = request.POST.get('tartalom')

        felhasznalo = None
        if felhasznalo_id:
            felhasznalo = Felhasznalo.objects.get(id=felhasznalo_id)

        csoport = None
        if csoport_id:
            csoport = Csoport.objects.get(id=csoport_id)

        if kuldesi_ido:
            kuldesi_ido = datetime.strptime(kuldesi_ido, "%Y-%m-%dT%H:%M")

        uj_uzenet = Uzenet(
            felhasznalo=felhasznalo,
            csoport=csoport,
            kuldesi_ido=kuldesi_ido,
            tartalom=tartalom
        )
        uj_uzenet.save()

        return redirect('index')

    else:
        felhasznalok = Felhasznalo.objects.all()
        csoportok = Csoport.objects.all()
        return render(request, 'admin/uzenet.html', {
            'felhasznalok': felhasznalok,
            'csoportok': csoportok
        })