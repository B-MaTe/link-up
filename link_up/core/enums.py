import enum


class BejegyzesResponse(enum.Enum):
    PROFANITY = 1,
    SUCCESS = 2,
    FILE_FORMAT_ERROR = 3,
    ERROR = 4

class ImageCreationResponse(enum.Enum):
    SUCCESS = 1,
    NOT_SUPPORTED_FILE_FORMAT = 2,
    ERROR = 3


def from_string(status: str) -> 'KapcsolatStatus':
    status = status.lower().strip() if status else ''
    if status == 'pending':
        return KapcsolatStatus.PENDING
    if status == 'accepted':
        return KapcsolatStatus.ACCEPTED
    if status == 'rejected':
        return KapcsolatStatus.REJECTED
    return KapcsolatStatus.NONE


class KapcsolatStatus(enum.Enum):
    PENDING = 1,
    ACCEPTED = 2,
    REJECTED = 3,
    NONE = 4

