from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import path

from . import admin_views
from .models import Felhasznalo


class AdminSite(admin.AdminSite):
    app_index_template = 'admin/custom_index.html'
    index_template = 'admin/custom_index.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [

            path('bejegyzes/', self.admin_view(admin_views.bejegyzes), name='bejegyzes'),
            path('csoport/', self.admin_view(admin_views.csoport), name='csoport'),
            path('komment/', self.admin_view(admin_views.komment), name='komment'),
            path('uzenet/', self.admin_view(admin_views.uzenet), name='uzenet'),
        ]
        print(urls)
        return custom_urls + urls


class FelhasznaloCreationForm(forms.ModelForm):
    """Form for creating new users in the admin."""
    jelszo1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    jelszo2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Felhasznalo
        fields = ('felhasznalonev',)

    def clean_jelszo2(self):
        password1 = self.cleaned_data.get("jelszo1")
        password2 = self.cleaned_data.get("jelszo2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["jelszo1"])
        if commit:
            user.save()
        return user


class FelhasznaloChangeForm(forms.ModelForm):
    """Form for updating users in the admin."""
    jelszo = ReadOnlyPasswordHashField(label="Password")

    class Meta:
        model = Felhasznalo
        fields = ('felhasznalonev', 'jelszo', 'admin', 'groups', 'user_permissions')

    def clean_jelszo(self):
        return self.initial["jelszo"]


class FelhasznaloAdmin(UserAdmin):
    form = FelhasznaloChangeForm
    add_form = FelhasznaloCreationForm

    model = Felhasznalo
    list_display = ('felhasznalonev', 'admin')
    list_filter = ('admin',)

    fieldsets = (
        (None, {'fields': ('felhasznalonev', 'jelszo')}),
        ('Permissions', {'fields': ('admin', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('felhasznalonev', 'jelszo1', 'jelszo2')}
        ),
    )

    search_fields = ('felhasznalonev',)
    ordering = ('felhasznalonev',)
    filter_horizontal = ('groups', 'user_permissions',)


admin_site = AdminSite()

admin_site.register(Felhasznalo, FelhasznaloAdmin)
