# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Felhasznalo
from django.utils.translation import gettext_lazy as _



class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Felhasználónév",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Jelszó",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    error_messages = {
        'invalid_login': _(
            "Hibás felhasználónév vagy jelszó. Próbáld újra."
        ),
        'inactive': _("Ez a fiók inaktív."),
    }


class CustomRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Jelszó",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Jelszó megerősítése",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    # email = forms.EmailField(
    #     label="Email",
    #     widget=forms.EmailInput(attrs={'class': 'form-control'})
    # )

    class Meta:
        model = Felhasznalo
        fields = ['felhasznalonev']
        widgets = {
            'felhasznalonev': forms.TextInput(attrs={'class': 'form-control'}),
        }

    error_messages = {
        'password_mismatch': _("A két jelszó nem egyezik."),
        'duplicate_username': _("Ez a felhasználónév már foglalt."),
        # 'duplicate_email': _("Ez az email cím már regisztrálva van."),
    }

    def clean_felhasznalonev(self):
        felhasznalonev = self.cleaned_data.get('felhasznalonev')
        if Felhasznalo.objects.filter(felhasznalonev=felhasznalonev).exists():
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
            )
        return felhasznalonev

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if Felhasznalo.objects.filter(email=email).exists():
    #         raise forms.ValidationError(
    #             self.error_messages['duplicate_email'],
    #             code='duplicate_email',
    #         )
    #     return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        jelszo = self.cleaned_data["password1"]
        felhasznalonev = self.cleaned_data["felhasznalonev"]
        if commit:
            user = Felhasznalo.objects.create_user(felhasznalonev=felhasznalonev, jelszo=jelszo)
            user.save()
        return user
