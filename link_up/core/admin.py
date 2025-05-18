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
            path('bejegyzes/', self.admin_view(admin_views.bejegyzes_list), name='bejegyzes'),
            path('bejegyzes/add/', self.admin_view(admin_views.bejegyzes), name='bejegyzes_add'),
            path('bejegyzes/<int:pk>/edit/', self.admin_view(admin_views.bejegyzes), name='bejegyzes_edit'),
            path('bejegyzes/<int:pk>/delete/', self.admin_view(admin_views.bejegyzes_delete), name='bejegyzes_delete'),

            path('csoport/', self.admin_view(admin_views.csoport_list), name='csoport'),
            path('csoport/add/', self.admin_view(admin_views.csoport), name='csoport_add'),
            path('csoport/<int:pk>/edit/', self.admin_view(admin_views.csoport), name='csoport_edit'),
            path('csoport/<int:pk>/delete/', self.admin_view(admin_views.csoport_delete), name='csoport_delete'),

            path('komment/', self.admin_view(admin_views.komment_list), name='komment'),
            path('komment/add/', self.admin_view(admin_views.komment), name='komment_add'),
            path('komment/<int:pk>/edit/', self.admin_view(admin_views.komment), name='komment_edit'),
            path('komment/<int:pk>/delete/', self.admin_view(admin_views.komment_delete), name='komment_delete'),

            path('uzenet/', self.admin_view(admin_views.uzenet_list), name='uzenet'),
            path('uzenet/add/', self.admin_view(admin_views.uzenet), name='uzenet_add'),
            path('uzenet/<int:pk>/edit/', self.admin_view(admin_views.uzenet), name='uzenet_edit'),
            path('uzenet/<int:pk>/delete/', self.admin_view(admin_views.uzenet_delete), name='uzenet_delete'),
        ]
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
    password = ReadOnlyPasswordHashField(label="Password")

    class Meta:
        model = Felhasznalo
        fields = ('felhasznalonev', 'password', 'admin', 'groups', 'user_permissions')



class FelhasznaloAdmin(UserAdmin):
    form = FelhasznaloChangeForm
    add_form = FelhasznaloCreationForm

    model = Felhasznalo
    list_display = ('felhasznalonev', 'admin')
    list_filter = ('admin',)

    fieldsets = (
        (None, {'fields': ('felhasznalonev', 'password')}),
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
