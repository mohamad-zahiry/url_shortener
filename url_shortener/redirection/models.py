from django.db import models
from django.utils import timezone

from shortener.models import ShortenedUrl


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name if self.name else "No Country"


def now_timeframe():
    return timezone.now().hour // 2 * 2


class UrlData(models.Model):
    TIME_FRAMES = [
        (0, "00:00-01:59"),
        (2, "02:00-03:59"),
        (4, "04:00-05:59"),
        (6, "06:00-07:59"),
        (8, "08:00-09:59"),
        (10, "10:00-11:59"),
        (12, "12:00-13:59"),
        (14, "14:00-15:59"),
        (16, "16:00-17:59"),
        (18, "18:00-19:59"),
        (20, "20:00-21:59"),
        (22, "22:00-23:59"),
    ]

    key = models.ForeignKey(
        to=ShortenedUrl,
        to_field="key",
        on_delete=models.CASCADE,
        editable=False,
    )
    visits = models.IntegerField(default=0)
    country = models.ForeignKey(
        to=Country,
        to_field="name",
        # default="",
        on_delete=models.DO_NOTHING,
        editable=False,
    )
    date = models.DateField(auto_now_add=True, editable=False)
    hour = models.IntegerField(
        choices=TIME_FRAMES,
        default=now_timeframe,
        editable=False,
    )

    class Meta:
        ordering = ["-date", "key", "-visits"]
        get_latest_by = "date"
        verbose_name_plural = "Urls Data"

    def __str__(self):
        # e.g: "[2022-08-10_08:00-09:59] /9rMLYWU6 (5) 'Iran'"
        return "[%s_%s] /%s (%s) '%s'" % (
            self.date,
            self.get_hour_display(),
            self.key,
            self.visits,
            self.country,
        )
