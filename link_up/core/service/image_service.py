import os
import uuid

from django.core.files.base import ContentFile

from core.enums import ImageCreationResponse
from link_up import settings


def create_image(image, sub_location):
    response = ImageCreationResponse.SUCCESS
    file_name = ""

    try:
        allowed_extensions = settings.ACCEPTED_IMAGE_EXTENSIONS
        kiterjesztes = os.path.splitext(image.name)[1].lower().replace(".", "")
        if kiterjesztes not in allowed_extensions:
            response = ImageCreationResponse.NOT_SUPPORTED_FILE_FORMAT
        else:
            kep_uuid = str(uuid.uuid4())
            file_name = f"{kep_uuid}.{kiterjesztes}"
            final_path = os.path.join('static', 'img', sub_location, file_name)

            file_content = ContentFile(image.read())
            full_path = os.path.join(settings.BASE_DIR, "core", final_path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'wb') as destination:
                destination.write(file_content.read())
    except Exception as e:
        print(e)
        response = ImageCreationResponse.ERROR
    return response, file_name