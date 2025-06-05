from datetime import datetime

from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from core.enums import ImageCreationResponse
from core.models import Felhasznalo, Bejegyzes, Csoport, Komment, Uzenet
from core.service import image_service
from core.utils import none_or_invalid, none_or_empty


def bejegyzes_list(request):
    bejegyzesek = Bejegyzes.objects.all()
    return render(request, 'admin/bejegyzes/bejegyzes_list.html', {'bejegyzesek': bejegyzesek})


def bejegyzes_delete(request, pk):
    Bejegyzes.objects.get(id=pk).delete()
    return redirect('admin:bejegyzes')

#admin views
def bejegyzes(request, pk=None):
    if pk:
        bejegyzes_instance = get_object_or_404(Bejegyzes, pk=pk)
        is_edit = True
    else:
        bejegyzes_instance = None
        is_edit = False

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
            response, uj_fajlnev = image_service.create_image(feltoltott_kep, 'post')
            if response == ImageCreationResponse.ERROR:
                errors.append('Kép feltöltése sikertelen.')
            elif response == ImageCreationResponse.NOT_SUPPORTED_FILE_FORMAT:
                errors.append('Nem megengedett kiterjesztés.')
        else:
            errors.append('Kép megadása kötelező.')

        if errors:
            return render(request, "admin/bejegyzes/bejegyzes.html", {
                'felhasznalok': Felhasznalo.objects.all(),
                'errors': errors,
                'input': {
                    'felhasznalo_id': felhasznalo_id,
                    'letrehozasi_ido': request.POST.get('letrehozasi_ido', ''),
                    'tartalom': tartalom,
                },
                'is_edit': is_edit,
                'bejegyzes': bejegyzes_instance,
            })

        if is_edit:
            bejegyzes_instance.felhasznalo = felhasznalo
            bejegyzes_instance.feltoltott_kep = uj_fajlnev
            bejegyzes_instance.letrehozasi_ido = letrehozasi_ido
            bejegyzes_instance.tartalom = tartalom
            bejegyzes_instance.save()

        else:
            Bejegyzes.objects.create(
                felhasznalo=felhasznalo,
                feltoltott_kep=uj_fajlnev,
                letrehozasi_ido=letrehozasi_ido,
                tartalom=tartalom
            )

        return redirect('admin:bejegyzes')
    else:
        felhasznalok = Felhasznalo.objects.all()
        if is_edit:
            input_data = {
                'felhasznalo_id': bejegyzes_instance.felhasznalo.id if bejegyzes_instance.felhasznalo else '',
                'letrehozasi_ido': bejegyzes_instance.letrehozasi_ido.strftime(
                    "%Y-%m-%dT%H:%M") if bejegyzes_instance.letrehozasi_ido else '',
                'tartalom': bejegyzes_instance.tartalom if bejegyzes_instance.tartalom else '',
            }
        else:
            input_data = {}
        return render(request, "admin/bejegyzes/bejegyzes.html", {
            'felhasznalok': felhasznalok,
            'input': input_data,
            'is_edit': is_edit,
            'bejegyzes': bejegyzes_instance,
        })

def csoport_list(request):
    csoportok = Csoport.objects.all()
    return render(request, 'admin/csoport/csoport_list.html', {'csoportok': csoportok})


def csoport_delete(request, pk):
    Csoport.objects.get(id=pk).delete()
    return redirect('admin:csoport')

def csoport(request, pk=None):
    if pk:
        csoport_instance = get_object_or_404(Csoport, id=pk)
        is_edit = True
    else:
        csoport_instance = None
        is_edit = False

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
            return render(request, 'admin/csoport/csoport.html', {
                'felhasznalok': Felhasznalo.objects.all(),
                'errors': errors,
                'input': {
                    'felhasznalo_id': felhasznalo_id,
                    'letrehozas_ido': request.POST.get('letrehozas_ido', ''),
                },
                'is_edit': is_edit,
                'csoport': csoport_instance,
            })

        if is_edit:
            csoport_instance.felhasznalo = felhasznalo
            csoport_instance.letrehozas_ido = letrehozas_ido
            csoport_instance.save()
        else:
            Csoport.objects.create(
                felhasznalo=felhasznalo,
                letrehozas_ido=letrehozas_ido
            )

        return redirect('admin:csoport')
    else:
        felhasznalok = Felhasznalo.objects.all()

        if is_edit:
            input_data = {
                'felhasznalo_id': csoport_instance.felhasznalo.id if csoport_instance.felhasznalo else '',
                'letrehozas_ido': csoport_instance.letrehozas_ido.strftime(
                    "%Y-%m-%dT%H:%M") if csoport_instance.letrehozas_ido else '',
            }
        else:
            input_data = {}
        return render(request, 'admin/csoport/csoport.html', {
            'felhasznalok': felhasznalok,
            'input': input_data,
            'is_edit': is_edit,
            'csoport': csoport_instance
        })


def komment_list(request):
    kommentek = Komment.objects.all()
    return render(request, 'admin/komment/komment_list.html', {'kommentek': kommentek})


def komment_delete(request, pk):
    Komment.objects.get(id=pk).delete()
    return redirect('admin:komment')


def komment(request, pk=None):
    if pk:
        komment_instance = get_object_or_404(Komment, id=pk)
        is_edit = True
    else:
        komment_instance = None
        is_edit = False

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
            return render(request, 'admin/komment/komment.html', {
                'bejegyzesek': bejegyzesek,
                'felhasznalok': felhasznalok,
                'errors': errors,
                'input': {
                    'felhasznalo_id': felhasznalo_id,
                    'bejegyzes_id': bejegyzes_id,
                    'feltoltesi_ido': request.POST.get('feltoltesi_ido', ''),
                    'tartalom': tartalom,
                },
                'is_edit': is_edit,
                'komment': komment_instance,
            })

        if is_edit:
            komment_instance.felhasznalo = felhasznalo
            komment_instance.bejegyzes = komment_bejegyzes
            komment_instance.feltoltesi_ido = feltoltesi_ido
            komment_instance.tartalom = tartalom
            komment_instance.save()
        else:
            Komment.objects.create(
                felhasznalo=felhasznalo,
                bejegyzes=komment_bejegyzes,
                feltoltesi_ido=feltoltesi_ido,
                tartalom=tartalom
            )

        return redirect('admin:komment')

    else:
        bejegyzesek = Bejegyzes.objects.all()
        felhasznalok = Felhasznalo.objects.all()

        if is_edit:
            input_data = {
                'felhasznalo_id': komment_instance.felhasznalo.id if komment_instance.felhasznalo else None,
                'bejegyzes_id': komment_instance.bejegyzes.id if komment_instance.bejegyzes else None,
                'feltoltesi_ido': komment_instance.feltoltesi_ido.strftime("%Y-%m-%dT%H:%M") if komment_instance.feltoltesi_ido else '',
                'tartalom': komment_instance.tartalom if komment_instance.tartalom else '',
            }
        else:
            input_data = {}

        return render(request, 'admin/komment/komment.html', {
            'bejegyzesek': bejegyzesek,
            'felhasznalok': felhasznalok,
            'input': input_data,
            'is_edit': is_edit,
            'komment': komment_instance,
        })


def uzenet(request, pk=None):
    if pk:
        uzenet_instance = get_object_or_404(Uzenet, pk=pk)
        is_edit = True
    else:
        uzenet_instance = None
        is_edit = False

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
            errors.append('Küldési idő megadása kötelező.')
            kuldesi_ido = None

        if none_or_empty(tartalom):
            errors.append('Tartalom megadása kötelező.')

        if errors:
            felhasznalok = Felhasznalo.objects.all()
            csoportok = Csoport.objects.all()
            return render(request, 'admin/uzenet/uzenet.html', {
                'felhasznalok': felhasznalok,
                'csoportok': csoportok,
                'errors': errors,
                'input': {
                    'felhasznalo_id': felhasznalo_id,
                    'csoport_id': csoport_id,
                    'kuldesi_ido': request.POST.get('kuldesi_ido', ''),
                    'tartalom': tartalom,
                },
                'is_edit': is_edit,
                'uzenet': uzenet_instance,
            })

        if is_edit:
            uzenet_instance.felhasznalo = felhasznalo
            uzenet_instance.csoport = csoport
            uzenet_instance.kuldesi_ido = kuldesi_ido
            uzenet_instance.tartalom = tartalom
            uzenet_instance.save()
        else:
            Uzenet.objects.create(
                felhasznalo=felhasznalo,
                csoport=csoport,
                kuldesi_ido=kuldesi_ido,
                tartalom=tartalom
            )

        return redirect('admin:uzenet')
    else:
        felhasznalok = Felhasznalo.objects.all()
        csoportok = Csoport.objects.all()
        if is_edit:
            input_data = {
                'felhasznalo_id': uzenet_instance.felhasznalo.id if uzenet_instance.felhasznalo else '',
                'csoport_id': uzenet_instance.csoport.id if uzenet_instance.csoport else '',
                'kuldesi_ido': uzenet_instance.kuldesi_ido.strftime(
                    "%Y-%m-%dT%H:%M") if uzenet_instance.kuldesi_ido else '',
                'tartalom': uzenet_instance.tartalom or '',
            }
        else:
            input_data = {}

        return render(request, 'admin/uzenet/uzenet.html', {
            'felhasznalok': felhasznalok,
            'csoportok': csoportok,
            'input': input_data,
            'is_edit': is_edit,
            'uzenet': uzenet_instance,
        })


def uzenet_delete(request, pk):
    Uzenet.objects.get(id=pk).delete()
    return redirect('admin:uzenet')


def uzenet_list(request):
    uzenetek = Uzenet.objects.all()
    return render(request, 'admin/uzenet/uzenet_list.html', {
        'uzenetek': uzenetek
    })


def admin_osszegzes(request):
    with connection.cursor() as cursor:
        first = cursor.var(int).var
        second = cursor.var(int).var
        third = cursor.var(int).var
        fourth = cursor.var(int).var
        fifth = cursor.var(int).var
        sixth = cursor.var(int).var
        cursor.callproc('summarize_admin_dashboard', [first, second, third, fourth, fifth, sixth])

        results = [first.getvalue(), second.getvalue(), third.getvalue(), fourth.getvalue(), fifth.getvalue(), sixth.getvalue()]


    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT f.felhasznalonev, COUNT(k.id) AS kommentek_szama
            FROM Felhasznalok f
            JOIN Kommentek k ON f.id = k.felhasznalo_id
            GROUP BY f.felhasznalonev
            ORDER BY kommentek_szama DESC
            FETCH FIRST 10 ROWS ONLY
        """)
        komment_aktivitas = cursor.fetchall()

        cursor.execute("""
            SELECT c.csoport_nev, COUNT(b.id) AS bejegyzes_szam
            FROM Csoportok c
            JOIN Bejegyzesek b ON c.id = b.felhasznalo_id
            GROUP BY c.csoport_nev
            ORDER BY bejegyzes_szam DESC
        """)
        csoport_bejegyzesek = cursor.fetchall()

        cursor.execute("""
            SELECT DISTINCT f.felhasznalonev
            FROM Felhasznalok f
            JOIN Csoportok c ON f.id = c.felhasznalo_id
            WHERE c.privat_beszelgetes = 1
        """)
        privat_felhasznalok = cursor.fetchall()

        cursor.execute("""
            SELECT f.felhasznalonev, AVG(LENGTH(k.tartalom)) AS atlag_komment_hossz
            FROM Felhasznalok f
            JOIN Kommentek k ON f.id = k.felhasznalo_id
            GROUP BY f.felhasznalonev
            ORDER BY atlag_komment_hossz DESC
        """)
        komment_hossz = cursor.fetchall()

        current_month = datetime.now().strftime("%Y-%m")

        cursor.execute("""
            WITH TargetMonth AS (
                SELECT 
                    TO_DATE(:current_month, 'YYYY-MM') AS start_date,
                    LAST_DAY(TO_DATE(:current_month, 'YYYY-MM')) AS end_date
                FROM DUAL
            )
            SELECT 
                c.id AS csoport_id,
                c.csoport_nev,
                COUNT(u.id) AS uzenetek_szama
            FROM 
                Csoportok c
            JOIN Uzenetek u ON c.id = u.csoport_id
            JOIN TargetMonth tm 
                ON u.kuldesi_ido BETWEEN tm.start_date AND tm.end_date
            WHERE 
                c.id IN (
                    SELECT csoport_id
                    FROM Felhasznalo_Csoportok
                    GROUP BY csoport_id
                    HAVING COUNT(felhasznalo_id) >= 10
                )
                AND EXISTS (
                    SELECT 1
                    FROM Felhasznalo_Csoportok fc
                    JOIN Felhasznalok f ON fc.felhasznalo_id = f.id
                    WHERE fc.csoport_id = c.id
                    AND f.admin = 1
                )
            GROUP BY c.id, c.csoport_nev
            ORDER BY uzenetek_szama DESC
        """, {'current_month': current_month})

        # Then get only the first row in Python
        honap_legtobb_uzenet_csoport = cursor.fetchone()

        now = datetime.now()
        current_year = now.strftime('%Y')
        current_month = now.strftime('%m')

        cursor.execute("""
            WITH ActivitySummary AS (
                SELECT 
                    felhasznalo_id,
                    COUNT(*) AS activity_count
                FROM (
                    SELECT felhasznalo_id FROM Uzenetek
                    WHERE EXTRACT(YEAR FROM kuldesi_ido) = :year
                      AND EXTRACT(MONTH FROM kuldesi_ido) = :month
                    UNION ALL
                    SELECT felhasznalo_id FROM Kommentek
                    WHERE EXTRACT(YEAR FROM feltoltesi_ido) = :year
                      AND EXTRACT(MONTH FROM feltoltesi_ido) = :month
                )
                GROUP BY felhasznalo_id
            )
            SELECT 
                f.id,
                f.felhasznalonev,
                a.activity_count
            FROM ActivitySummary a
            JOIN Felhasznalok f ON a.felhasznalo_id = f.id
            WHERE ROWNUM <= 3
            ORDER BY a.activity_count DESC
        """, {'year': current_year, 'month': current_month})

        honap_legtobb_uzenet_top_3 = cursor.fetchall()

        cursor.execute("""
            WITH AktivFelhasznalok AS (
                SELECT 
                    f.id,
                    f.felhasznalonev,
                    COUNT(u.id) AS uzenetek_szama
                FROM 
                    Felhasznalok f
                JOIN Uzenetek u ON f.id = u.felhasznalo_id
                WHERE 
                    u.kuldesi_ido >= ADD_MONTHS(TRUNC(SYSDATE, 'MM'), -1)
                    AND u.kuldesi_ido < TRUNC(SYSDATE, 'MM')
                GROUP BY f.id, f.felhasznalonev
                HAVING COUNT(u.id) >= 5
            )
            SELECT 
                af.felhasznalonev,
                af.uzenetek_szama,
                TO_CHAR(f.utolso_bejelentkezes, 'YYYY-MM-DD HH24:MI') AS utolso_bejelentkezes
            FROM 
                AktivFelhasznalok af
            JOIN Felhasznalok f ON af.id = f.id
            ORDER BY af.uzenetek_szama DESC
        """)

        aktiv_felhasznalok = cursor.fetchall()

        cursor.execute("""
            WITH AdminCsoportTagok AS (
                SELECT 
                    fc.csoport_id,
                    COUNT(*) AS admin_db
                FROM Felhasznalo_Csoportok fc
                JOIN Felhasznalok f ON fc.felhasznalo_id = f.id
                WHERE f.admin = 1
                GROUP BY fc.csoport_id
                HAVING COUNT(*) > 3
            ),
            BejegyzesSzamok AS (
                SELECT 
                    c.id AS csoport_id,
                    COUNT(b.id) AS bejegyzesek_szama
                FROM Csoportok c
                JOIN Felhasznalo_Csoportok fc ON c.id = fc.csoport_id
                JOIN Bejegyzesek b ON fc.felhasznalo_id = b.felhasznalo_id
                GROUP BY c.id
                HAVING COUNT(b.id) >= 10
            )
            SELECT 
                c.csoport_nev,
                a.admin_db,
                b.bejegyzesek_szama
            FROM AdminCsoportTagok a
            JOIN BejegyzesSzamok b ON a.csoport_id = b.csoport_id
            JOIN Csoportok c ON c.id = a.csoport_id
            ORDER BY b.bejegyzesek_szama DESC
        """)

        admin_aktiv_csoportok = cursor.fetchall()


        context = {
            'adminok_szama': results[0],
            'felhasznalok_szama': results[1],
            'csoportok_szama': results[2],
            'bejegyzesek_szama': results[3],
            'kommentek_szama': results[4],
            'uzenetek_szama': results[5],
            'komment_aktivitas': komment_aktivitas,
            'csoport_bejegyzesek': csoport_bejegyzesek,
            'privat_felhasznalok': privat_felhasznalok,
            'komment_hossz': komment_hossz,
            'honap_legtobb_uzenet_csoport': honap_legtobb_uzenet_csoport,
            'honap_legtobb_uzenet_top_3': honap_legtobb_uzenet_top_3,
            'aktiv_felhasznalok': aktiv_felhasznalok,
            'admin_aktiv_csoportok': admin_aktiv_csoportok
        }

    return render(request, 'admin/osszegzes.html', context)