def none_or_empty(value: str):
    return value is None or value.strip() == ''

def none_or_invalid(value: int, accept_zero=False):
    if value is None:
        return True

    value = int(value)
    return value < 0 or (not accept_zero and value == 0)