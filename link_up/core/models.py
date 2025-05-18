# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db import connection
from django.db.models import Q
from django.utils.timezone import now

from link_up.settings import STATIC_URL


class Bejegyzes(models.Model):
    id = models.AutoField(primary_key=True)
    felhasznalo = models.ForeignKey('Felhasznalo', models.DO_NOTHING, blank=True, null=True, related_name='bejegyzesek')
    feltoltott_kep = models.CharField(max_length=128, blank=True, null=True)
    letrehozasi_ido = models.DateTimeField(blank=True, null=True)
    tartalom = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bejegyzesek'


class Csoport(models.Model):
    id = models.AutoField(primary_key=True)
    felhasznalo = models.ForeignKey('Felhasznalo', models.DO_NOTHING, blank=True, null=True)
    letrehozas_ido = models.DateTimeField(blank=True, null=True)
    csoport_nev = models.CharField(max_length=128)
    privat_beszelgetes = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'csoportok'

    def get_other_participants(self):
        return Felhasznalo.objects.filter(
            felhasznalocssoport__csoport=self
        ).exclude(id=self.felhasznalo_id)

    def get_last_message(self):
        return Uzenet.objects.filter(csoport=self).order_by('-kuldesi_ido').first()

    def get_messages(self):
        return Uzenet.objects.filter(csoport=self).order_by('kuldesi_ido')


class FelhasznaloCsoport(models.Model):
    csoport = models.OneToOneField(Csoport, models.DO_NOTHING, primary_key=True)
    felhasznalo = models.ForeignKey('Felhasznalo', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'felhasznalo_csoportok'
        unique_together = (('csoport', 'felhasznalo'),)


class FelhasznaloKapcsolat(models.Model):
    jelolo = models.OneToOneField('Felhasznalo', models.DO_NOTHING, primary_key=True)
    jelolt = models.ForeignKey('Felhasznalo', models.DO_NOTHING, related_name='felhasznalokapcsolatok')
    statusz = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'felhasznalo_kapcsolatok'
        unique_together = (('jelolo', 'jelolt'),)


class FelhasznaloManager(BaseUserManager):
    def create_user(self, felhasznalonev, jelszo=None, **extra_fields):
        if not felhasznalonev:
            raise ValueError('The Username must be set')

        cursor = connection.cursor()
        cursor.execute("SELECT felhasznalok_seq.NEXTVAL FROM dual")
        user_id = cursor.fetchone()[0]

        user = self.model(id=user_id, felhasznalonev=felhasznalonev, **extra_fields)
        user.set_password(jelszo)
        user.csatlakozas_ido = now()
        user.utolso_bejelentkezes = now()
        user.save(using=self._db)
        return user

    def create_superuser(self, felhasznalonev, jelszo=None, **extra_fields):
        extra_fields.setdefault('admin', 1)
        return self.create_user(felhasznalonev, jelszo, **extra_fields)


class Felhasznalo(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    felhasznalonev = models.CharField(unique=True, max_length=50)
    jelszo = models.CharField(max_length=128)
    utolso_bejelentkezes = models.DateTimeField(blank=True, null=True)
    csatlakozas_ido = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    admin = models.BooleanField(null=True, blank=True, default=False)
    profil_kep = models.CharField(max_length=128, blank=True, null=True)

    objects = FelhasznaloManager()

    USERNAME_FIELD = 'felhasznalonev'
    REQUIRED_FIELDS = []

    class Meta:
        managed = False
        db_table = 'felhasznalok'
        verbose_name = 'Felhasznalo'
        verbose_name_plural = 'Felhasznalok'

    @property
    def password(self):
        return self.jelszo

    @password.setter
    def password(self, raw_password):
        self.jelszo = make_password(raw_password)

    @property
    def last_login(self):
        return self.utolso_bejelentkezes

    @property
    def is_staff(self):
        return self.admin is True

    @property
    def is_superuser(self):
        return self.admin is True

    @property
    def is_active(self):
        return True

    def get_friends(self):
        accepted_kapcsolatok = FelhasznaloKapcsolat.objects.filter(
            Q(jelolo=self) | Q(jelolt=self),
            statusz='accepted'
        )

        friends = []
        for kapcsolat in accepted_kapcsolatok:
            if kapcsolat.jelolo == self:
                friends.append(kapcsolat.jelolt)
            else:
                friends.append(kapcsolat.jelolo)
        return friends

    def __str__(self):
        return self.felhasznalonev


class Komment(models.Model):
    id = models.AutoField(primary_key=True)
    felhasznalo = models.ForeignKey(Felhasznalo, models.DO_NOTHING, blank=True, null=True)
    bejegyzes = models.ForeignKey(Bejegyzes, models.DO_NOTHING, blank=True, null=True)
    feltoltesi_ido = models.DateTimeField(blank=True, null=True)
    tartalom = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kommentek'


class Uzenet(models.Model):
    id = models.AutoField(primary_key=True)
    felhasznalo = models.ForeignKey(Felhasznalo, models.DO_NOTHING, blank=True, null=True)
    csoport = models.ForeignKey(Csoport, models.DO_NOTHING, blank=True, null=True)
    kuldesi_ido = models.DateTimeField(blank=True, null=True)
    tartalom = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uzenetek'
