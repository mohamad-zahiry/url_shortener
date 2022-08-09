from shortener.models import ShortenedUrl


class keyAsSlugMixin:
    """A Mixin that use 'key' as slug-field for ShortenedUrl model"""

    model = ShortenedUrl
    slug_field = "key"
    slug_url_kwarg = "key"
