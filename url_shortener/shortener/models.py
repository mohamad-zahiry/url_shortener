from django.db import models
from django.contrib.auth.models import User


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
