from core.enums import BejegyzesResponse
from core.models import Bejegyzes
from core.service.profanity_service import has_profanity


def create_bejegyzes(request, text, image=None) -> BejegyzesResponse:
    user = request.user

    profanity = has_profanity(text)

    if profanity:
        return BejegyzesResponse.PROFANITY

    # TODO: save image and add path to the bejegyzes
    try:
        Bejegyzes.objects.create(felhasznalo=user, tartalom=text)
    except Exception:
        return BejegyzesResponse.ERROR

    return BejegyzesResponse.SUCCESS
