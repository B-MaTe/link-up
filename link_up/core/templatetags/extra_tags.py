from django import template

from core.models import Bejegyzes, Felhasznalo

register = template.Library()


@register.filter(name='post_file_relative_path')
def post_file_relative_path(post: Bejegyzes):
    if post.feltoltott_kep:
        return f"img/post/{post.feltoltott_kep}"

    return ""


@register.filter(name='profile_kep_relative_path_or_default')
def profile_kep_relative_path_or_default(felhasznalo: Felhasznalo):
    base = "img/profile/"
    if felhasznalo.profil_kep:
        return f"{base}{felhasznalo.profil_kep}"

    return base + "profile.png"
