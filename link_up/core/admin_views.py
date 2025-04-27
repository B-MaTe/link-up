import os
import uuid
from datetime import datetime
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from core.models import Felhasznalo, Bejegyzes, Csoport, Komment, Uzenet
from core.utils import none_or_invalid, none_or_empty
from link_up import settings


#admin views
def bejegyzes(request):
    errors = []
    if request.method == 'POST':
        felhasznalo_id = request.POST.get('felhasznalo')
        feltoltott_kep = request.FILES.get('feltoltott_kep')
        letrehozasi_ido = request.POST.get('letrehozasi_ido')
        tartalom = request.POST.get('tartalom')

        if none_or_invalid(felhasznalo_id):
            errors.append('Felhasználó megadása kötelező.')
            felhasznalo = None
        else:
            try:
                felhasznalo = Felhasznalo.objects.get(id=int(felhasznalo_id))
            except (Felhasznalo.DoesNotExist, ValueError):
                errors.append('Érvénytelen felhasználó.')
                felhasznalo = None

        if not none_or_empty(letrehozasi_ido):
            try:
                letrehozasi_ido = datetime.strptime(letrehozasi_ido, "%Y-%m-%dT%H:%M")
            except ValueError:
                errors.append('Érvénytelen létrehozási idő formátum.')
                letrehozasi_ido = None
        else:
            errors.append('Letrehozás idő megadása kötelező.')
            letrehozasi_ido = None

        if none_or_empty(tartalom):
            errors.append('Tartalom megadása kötelező.')

        uj_fajlnev = None
        if feltoltott_kep:
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            kiterjesztes = os.path.splitext(feltoltott_kep.name)[1].lower()
            if kiterjesztes not in allowed_extensions:
                errors.append('Nem támogatott képformátum.')
            else:
                kep_uuid = str(uuid.uuid4())
                uj_fajlnev = f"{kep_uuid}{kiterjesztes}"
                cel_utvonal = os.path.join('static', 'img', uj_fajlnev)

                file_content = ContentFile(feltoltott_kep.read())
                full_path = os.path.join(settings.BASE_DIR, "core", cel_utvonal)

                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'wb') as destination:
                    destination.write(file_content.read())
        else:
            errors.append('Kép megadása kötelező.')

        if errors:
            return render(request, "admin/bejegyzes.html", {
                'felhasznalok': Felhasznalo.objects.all(),
                'errors': errors,
                'input': {
                    'felhasznalo_id': felhasznalo_id,
                    'letrehozasi_ido': request.POST.get('letrehozasi_ido', ''),
                    'tartalom': tartalom,
                }
            })

        Bejegyzes.objects.create(
            felhasznalo=felhasznalo,
            feltoltott_kep=uj_fajlnev,
            letrehozasi_ido=letrehozasi_ido,
            tartalom=tartalom
        )

        return redirect('index')

    return render(request, "admin/bejegyzes.html", {
        'felhasznalok': Felhasznalo.objects.all(),
    })


def csoport(request):
    errors = []
    if request.method == 'POST':
        felhasznalo_id = request.POST.get('felhasznalo')
        letrehozas_ido = request.POST.get('letrehozas_ido')

        if none_or_invalid(felhasznalo_id):
            errors.append('Felhasználó megadása kötelező.')
            felhasznalo = None
        else:
            try:
                felhasznalo = Felhasznalo.objects.get(id=int(felhasznalo_id))
            except (Felhasznalo.DoesNotExist, ValueError):
                errors.append('Érvénytelen felhasználó.')
                felhasznalo = None

        if not none_or_empty(letrehozas_ido):
            try:
                letrehozas_ido = datetime.strptime(letrehozas_ido, "%Y-%m-%dT%H:%M")
            except ValueError:
                errors.append('Érvénytelen létrehozási idő formátum.')
                letrehozas_ido = None
        else:
            errors.append('Létrehozás idő megadása Kötelező.')
            letrehozas_ido = None

        if errors:
            return render(request, 'admin/csoport.html', {
                'felhasznalok': Felhasznalo.objects.all(),
                'errors': errors,
                'input': {
                    'felhasznalo_id': felhasznalo_id,
                    'letrehozas_ido': request.POST.get('letrehozas_ido', ''),
                }
            })

        Csoport.objects.create(
            felhasznalo=felhasznalo,
            letrehozas_ido=letrehozas_ido
        )

        return redirect('index')

    return render(request, 'admin/csoport.html', {'felhasznalok': Felhasznalo.objects.all()})


def komment(request):
    errors = []
    if request.method == 'POST':
        felhasznalo_id = request.POST.get('felhasznalo')
        bejegyzes_id = request.POST.get('bejegyzes_id')
        feltoltesi_ido = request.POST.get('feltoltesi_ido')
        tartalom = request.POST.get('tartalom')

        if none_or_invalid(felhasznalo_id):
            errors.append('Felhasználó megadása kötelező.')
            felhasznalo = None
        else:
            try:
                felhasznalo = Felhasznalo.objects.get(id=int(felhasznalo_id))
            except (Felhasznalo.DoesNotExist, ValueError):
                errors.append('Érvénytelen felhasználó.')
                felhasznalo = None

        if none_or_invalid(bejegyzes_id):
            errors.append('Bejegyzés megadása kötelező.')
            komment_bejegyzes = None
        else:
            try:
                komment_bejegyzes = Bejegyzes.objects.get(id=int(bejegyzes_id))
            except (Bejegyzes.DoesNotExist, ValueError):
                errors.append('Érvénytelen bejegyzés.')
                komment_bejegyzes = None

        if not none_or_empty(feltoltesi_ido):
            try:
                feltoltesi_ido = datetime.strptime(feltoltesi_ido, "%Y-%m-%dT%H:%M")
            except ValueError:
                errors.append('Érvénytelen feltöltési idő formátum.')
                feltoltesi_ido = None
        else:
            errors.append('Feltöltési idő megadása Kötelező.')
            feltoltesi_ido = None

        if none_or_empty(tartalom):
            errors.append('Tartalom megadása kötelező.')

        if errors:
            bejegyzesek = Bejegyzes.objects.all()
            felhasznalok = Felhasznalo.objects.all()
            return render(request, 'admin/komment.html', {
                'bejegyzesek': bejegyzesek,
                'felhasznalok': felhasznalok,
                'errors': errors,
                'input': {
                    'felhasznalo_id': felhasznalo_id,
                    'bejegyzes_id': bejegyzes_id,
                    'feltoltesi_ido': request.POST.get('feltoltesi_ido', ''),
                    'tartalom': tartalom,
                }
            })

        Komment.objects.create(
            felhasznalo=felhasznalo,
            bejegyzes=komment_bejegyzes,
            feltoltesi_ido=feltoltesi_ido,
            tartalom=tartalom
        )

        return redirect('index')

    else:
        bejegyzesek = Bejegyzes.objects.all()
        felhasznalok = Felhasznalo.objects.all()
        return render(request, 'admin/komment.html', {
            'bejegyzesek': bejegyzesek,
            'felhasznalok': felhasznalok
        })


def uzenet(request):
    errors = []
    if request.method == 'POST':
        felhasznalo_id = request.POST.get('felhasznalo')
        csoport_id = request.POST.get('csoport')
        kuldesi_ido = request.POST.get('kuldesi_ido')
        tartalom = request.POST.get('tartalom')

        if none_or_invalid(felhasznalo_id):
            errors.append('Felhasználó megadása kötelező.')
            felhasznalo = None
        else:
            try:
                felhasznalo = Felhasznalo.objects.get(id=int(felhasznalo_id))
            except (Felhasznalo.DoesNotExist, ValueError):
                errors.append('Érvénytelen felhasználó.')
                felhasznalo = None

        if none_or_invalid(csoport_id):
            errors.append('Csoport megadása kötelező.')
            csoport = None
        else:
            try:
                csoport = Csoport.objects.get(id=int(csoport_id))
            except (Csoport.DoesNotExist, ValueError):
                errors.append('Érvénytelen csoport.')
                csoport = None

        if not none_or_empty(kuldesi_ido):
            try:
                kuldesi_ido = datetime.strptime(kuldesi_ido, "%Y-%m-%dT%H:%M")
            except ValueError:
                errors.append('Érvénytelen küldési idő formátum.')
                kuldesi_ido = None
        else:
            errors.append('Küldési idő megadása Kötelező.')
            kuldesi_ido = None

        if none_or_empty(tartalom):
            errors.append('Tartalom megadása kötelező.')

        if errors:
            felhasznalok = Felhasznalo.objects.all()
            csoportok = Csoport.objects.all()
            return render(request, 'admin/uzenet.html', {
                'felhasznalok': felhasznalok,
                'csoportok': csoportok,
                'errors': errors,
                'input': {
                    'felhasznalo_id': felhasznalo_id,
                    'csoport_id': csoport_id,
                    'kuldesi_ido': request.POST.get('kuldesi_ido', ''),
                    'tartalom': tartalom,
                }
            })

        Uzenet.objects.create(
            felhasznalo=felhasznalo,
            csoport=csoport,
            kuldesi_ido=kuldesi_ido,
            tartalom=tartalom
        )

        return redirect('index')

    else:
        felhasznalok = Felhasznalo.objects.all()
        csoportok = Csoport.objects.all()
        return render(request, 'admin/uzenet.html', {
            'felhasznalok': felhasznalok,
            'csoportok': csoportok
        })
