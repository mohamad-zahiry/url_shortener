import string
import secrets

CHARS = string.ascii_letters + string.digits
DEFAULT_SIZE = 8
MAX_KEY_SIZE = 15
MIN_KEY_SIZE = 3


def short_url(size=DEFAULT_SIZE):
    if size < MIN_KEY_SIZE:
        size = MIN_KEY_SIZE
    elif size > MAX_KEY_SIZE:
        size = MAX_KEY_SIZE

    return "".join(secrets.choice(CHARS) for _ in range(size))
