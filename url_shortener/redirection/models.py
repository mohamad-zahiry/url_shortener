from django.db import models
from django.utils import timezone

from shortener.models import ShortenedUrl
from redirection.utils.url_data import now_timeframe


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)


def now_timeframe():
    """Converts the current time to the "TIME FRAMES" key"""
    return timezone.now().hour // 2 * 2


class UrlData(models.Model):
    TIME_FRAMES = [
        (0, "00:00 - 01:59"),
        (2, "02:00 - 03:59"),
        (4, "04:00 - 05:59"),
        (6, "06:00 - 07:59"),
        (8, "08:00 - 09:59"),
        (10, "10:00 - 11:59"),
        (12, "12:00 - 13:59"),
        (14, "14:00 - 15:59"),
        (16, "16:00 - 17:59"),
        (18, "18:00 - 19:59"),
        (20, "20:00 - 21:59"),
        (22, "22:00 - 23:59"),
    ]

    key = models.ForeignKey(to=ShortenedUrl, to_field="key", on_delete=models.CASCADE)
    visits = models.IntegerField(default=0)
    country = models.ForeignKey(to=Country, on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now_add=True)
    hour = models.IntegerField(choices=TIME_FRAMES, default=now_timeframe)
