from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    DateTimeField,
    URLField,
    DurationField,
    BooleanField,
)
from django.utils import timezone

from Ushort.models import Url


class UrlCreateSerializer(ModelSerializer):
    url = CharField(max_length=10)
    target = URLField()

    access_start = DateTimeField(default=timezone.now)
    access_duration = DurationField(default=timezone.timedelta(days=10))
    access_code = CharField(max_length=64, default="", allow_blank=True)

    monitored = BooleanField(default=False)

    class Meta:
        model = Url
        fields = ["url", "target", "access_start", "access_duration", "access_code", "monitored"]


class UrlListSerializer(ModelSerializer):
    expired = BooleanField(source="is_expired")

    class Meta:
        model = Url
        fields = ["url", "target", "visitors", "expired"]
