from datetime import datetime

from core.enums import BejegyzesResponse, ImageCreationResponse, UzenetResponse
from core.models import Bejegyzes
from core.service import image_service
from core.service.profanity_service import has_profanity


def create_bejegyzes(request, text, image=None) -> BejegyzesResponse:
    user = request.user

    profanity = has_profanity(text)

    if profanity:
        return BejegyzesResponse.PROFANITY

    file_name = None
    if image:
        response, file_name = image_service.create_image(image, "post")
        if response == ImageCreationResponse.NOT_SUPPORTED_FILE_FORMAT:
            return BejegyzesResponse.FILE_FORMAT_ERROR

        if response == ImageCreationResponse.ERROR:
            return BejegyzesResponse.ERROR
    try:
        Bejegyzes.objects.create(felhasznalo=user, tartalom=text, feltoltott_kep=file_name, letrehozasi_ido=datetime.now())
    except Exception:
        return BejegyzesResponse.ERROR

    return BejegyzesResponse.SUCCESS


def add_komment(bejegyzes, user, text):
    profanity = has_profanity(text)

    if profanity:
        return UzenetResponse.PROFANITY

    try:
        bejegyzes.kommentek.create(felhasznalo=user, tartalom=text, feltoltesi_ido=datetime.now())
    except Exception:
        return UzenetResponse.ERROR

    return UzenetResponse.SUCCESS
