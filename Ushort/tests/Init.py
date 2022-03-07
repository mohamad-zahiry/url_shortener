from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.utils import timezone as tz
from django.core.exceptions import ValidationError
from Ushort.models import Creator, Url, Country, Visitor


class Init(TestCase):
    __url_unique_number = -1  # counter of UUrl method

    def setUp(self):
        self.user = User.objects.create(username="user", email="user@email.com", password="password")
        self.creator = Creator.objects.create(user=self.user, email=self.user.email)
        self.target = "https://google.com"
        self.request_factory = RequestFactory()

    def tearDown(self):
        for url in Url.objects.all():
            url.delete()
        self.creator.set_Free_Account()
        return super().tearDown()

    def UUrl(self):
        # ? Generate unique url in order
        Init.__url_unique_number += 1
        return hex(Init.__url_unique_number)[2:]

    def make_url(self, save=False, **kwargs):
        kwa = {
            "url": self.UUrl(),
            "target": self.target,
            "creator": self.creator,
            "access_start": tz.now(),
            "access_duration": tz.timedelta(days=10),
            "access_code": "",
        }
        kwa.update(kwargs)
        obj = Url(**kwa)

        if save:
            obj.save()

        return obj
