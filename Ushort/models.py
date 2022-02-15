from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Creator(models.Model):
    """This model represents the User-model with some additional functions and uses email as the username"""

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    max_url_a_day = models.IntegerField(default=5, help_text="Maximum number of URLs a creator can generate per day")
    max_url = models.IntegerField(default=25, help_text="Maximum number of URLs a creator can generate")

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def can_generate_url(self):
        if self.url_set.all().count() <= self.max_url:
            return True
        return False

    @property
    def can_generate_url_tody(self):
        last_day = timezone.now() + timezone.timedelta(days=-1)
        last_day_urls_count = self.url_set.filter(created__gte=last_day).count()

        if last_day_urls_count < self.max_url_a_day:
            return True
        return False
