from django.forms import ModelForm, DateTimeField, DateTimeInput

from shortener.models import ShortenedUrl


class ShortenedUrlForm(ModelForm):
    active_from = DateTimeField(widget=DateTimeInput(attrs={"type": "datetime-local"}))
    active_until = DateTimeField(widget=DateTimeInput(attrs={"type": "datetime-local"}))

    class Meta:
        model = ShortenedUrl
        fields = ("url", "active_from", "active_until")
