from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from shortener.utils.shortener import short_url


class ShortenedUrl(models.Model):
    url = models.URLField(max_length=300)
    key = models.CharField(max_length=15, unique=True, blank=False)

    active_from = models.DateTimeField()
    active_until = models.DateTimeField()

    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        key = short_url()
        while ShortenedUrl.objects.filter(key=key).exists():
            key = short_url()
        self.key = key

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shortener:url_detail", kwargs={"key": self.key})
