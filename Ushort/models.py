from shutil import register_unpack_format
from django.db.models import (
    Model,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DurationField,
    EmailField,
    IntegerField,
    OneToOneField,
    TextField,
    URLField,
    ForeignKey,
    TextChoices,
    CASCADE,
    SET_NULL,
    DO_NOTHING,
)
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.http import HttpRequest
import ipware
import requests
import json


class Creator(Model):
    """This model represents the User-model with some additional functions and uses email as the username"""

    class Account:
        class Types(TextChoices):
            FREE = "F", _("Free")
            ADVANCED = "A", _("Advanced")
            COMPLETE = "C", _("Complete")

        class Free:
            max_url = 25
            max_url_a_day = 5
            max_monitored_url = 0

        class Advanced:
            max_url = 400
            max_url_a_day = 20
            max_monitored_url = 200

        class Complete:
            max_url = 1000
            max_url_a_day = 100
            max_monitored_url = 1000

    user = OneToOneField(to=User, on_delete=CASCADE)
    email = EmailField(unique=True)

    account_type = TextField(choices=Account.Types.choices, max_length=1, default=Account.Types.FREE)
    max_url = IntegerField(default=25, help_text="Maximum number of URLs a creator can generate")
    max_url_a_day = IntegerField(default=5, help_text="Maximum number of URLs a creator can generate per day")
    max_monitored_url = IntegerField(default=0, help_text="Maximum number of Monitored-URLs a creator can generate")

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def can_generate_url(self):
        if self.url_set.all().count() < self.max_url:
            return True
        return False

    @property
    def can_generate_url_tody(self):
        last_day = timezone.now() + timezone.timedelta(days=-1)
        last_day_urls_number = self.url_set.filter(created__gte=last_day).count()

        if last_day_urls_number < self.max_url_a_day:
            return True
        return False

    @property
    def can_generate_monitored_url(self):
        monitored_urls_number = self.url_set.filter(creator=self, monitored=True).count()
        if monitored_urls_number < self.max_monitored_url:
            return True
        return False

    @property
    def type(self):
        return self.get_account_type_display()

    @property
    def all_visitors(self):
        urls_visitors = Url.objects.filter(creator=self).only("visitors")
        return sum(u.visitors for u in urls_visitors)

    @property
    def simple_urls_number(self):
        return Url.objects.filter(creator=self, monitored=False).count()

    @property
    def monitored_urls_number(self):
        return Url.objects.filter(creator=self, monitored=True).count()

    @property
    def all_urls_number(self):
        return self.simple_urls_number + self.monitored_urls_number

    @property
    def active_urls_number(self):
        qs = Url.objects.filter(creator=self)
        return len(list(filter(lambda u: not u.is_expired, qs)))

    @property
    def expired_urls_number(self):
        qs = Url.objects.filter(creator=self)
        return len(list(filter(lambda u: u.is_expired, qs)))

    def set_Free_Account(self):
        self.account_type = Creator.Account.Types.FREE
        self.max_url = Creator.Account.Free.max_url
        self.max_url_a_day = Creator.Account.Free.max_url_a_day
        self.max_monitored_url = Creator.Account.Free.max_monitored_url
        self.save()

    def set_Advanced_Account(self):
        self.account_type = Creator.Account.Types.ADVANCED
        self.max_url = Creator.Account.Advanced.max_url
        self.max_url_a_day = Creator.Account.Advanced.max_url_a_day
        self.max_monitored_url = Creator.Account.Advanced.max_monitored_url
        self.save()

    def set_Complete_Account(self):
        self.account_type = Creator.Account.Types.COMPLETE
        self.max_url = Creator.Account.Complete.max_url
        self.max_url_a_day = Creator.Account.Complete.max_url_a_day
        self.max_monitored_url = Creator.Account.Complete.max_monitored_url
        self.save()

    def n_last_urls(self, num=None):
        qs = Url.objects.filter(creator=self)[:num]
        return qs[:num] if num is not None else qs

    @staticmethod
    def by_request(request):
        qs = Creator.objects.filter(user=request.user)
        if qs.count() == 1:
            return qs.first()
        return None


class Url(Model):
    url = CharField(max_length=10, unique=True)
    target = URLField()
    creator = ForeignKey(to=Creator, to_field="email", on_delete=DO_NOTHING)

    visitors = IntegerField(default=0)
    visitors_after_expire = IntegerField(default=0)

    access_start = DateTimeField(default=timezone.now)
    access_duration = DurationField(default=timezone.timedelta(days=10), help_text="Duration of access to the URL")
    access_code = CharField(max_length=64, default="", blank=True, null=True, help_text="Restricts access to this URL with the access code")

    monitored = BooleanField(default=False, help_text="If checked, time, date, country and number of visitors will be collected for the URL until it expires")

    created = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["creator", "-created"]
        get_latest_by = ["created"]

    def __str__(self):
        return f"/{self.url}"

    def clean(self):
        url = Url.objects.filter(id=self.id)
        if not url.exists():
            if not self.creator.can_generate_url:
                raise ValidationError(_(f"you only can create {self.creator.max_url} URLs"), code="max_url_creation")

            if not self.creator.can_generate_url_tody:
                raise ValidationError(_(f"you can create {self.creator.max_url_a_day} URLs a day"), code="max_url_creation_a_day")

            if self.monitored:
                if not self.creator.can_generate_monitored_url:
                    raise ValidationError(_(f"you can create {self.creator.max_monitored_url} monitored URLs"), code="max_monitored_url_creation")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def expire_time(self):
        return self.access_start + self.access_duration

    @property
    def is_started(self):
        if self.access_start <= timezone.now():
            return True
        return False

    @property
    def is_expired(self):
        if self.expire_time <= timezone.now():
            return True
        return False

    @property
    def expired_after(self):
        if self.is_expired:
            return timezone.timedelta()
        elif self.is_started:
            return self.expire_time - timezone.now()
        return self.access_duration  # if isn't started, returns the "Url.access_duration"

    @property
    def time_left_percent(self):
        if self.is_started:
            return round((timezone.now() - self.access_start) / self.access_duration * 100, 1)
        return 0

    @property
    def is_public(self):
        if self.access_code:
            return False
        return True

    @property
    def visitors_countries_list(self):
        return Country.countries_for_url(url=self)

    @property
    def most_country(self):
        return Visitor.for_url_most_country(url=self)

    @property
    def least_country(self):
        return Visitor.for_url_least_country(url=self)

    def check_access_code(self, access_code):
        if self.access_code == str(access_code):
            return True
        return False

    def add_visitor(self, request: HttpRequest):
        if self.is_expired:
            self.visitors_after_expire += 1
        else:

            if self.monitored:  # Visitor Model only used for "monitored" URLs
                ip, _ = ipware.get_client_ip(request)
                country = Country.country_by_ip(ip)
                Visitor.increase_or_create(url=self, country=country)

            self.visitors += 1

        self.save()


class Country(Model):
    # ? "-" used for the unknown IPs. The "name" field can't be empty because
    # ? of "Visitor" model, which use "Country.name" as "ForeignKey"
    name = CharField(max_length=50, unique=True, default="-")
    code = CharField(max_length=2, unique=True, default="-", help_text="ISO 3166-1 alpha-2 codes are two-letter country codes")

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return "No Country" if self.name == "-" else self.name

    def visitor_number(self):
        return Visitor.all_from_country(country=self)

    @staticmethod
    def __ip_to_country__ip_api(ip: str):
        name = code = "-"

        try:
            answer = requests.get(f"http://ip-api.com/json/{ip}?fields=country,countryCode").text
        except Exception:
            return (name, code)

        answer = json.loads(answer)
        if answer:
            name = answer.get("country")
            code = answer.get("countryCode")

        return (name, code)

    @classmethod
    def country_by_ip(cls, ip: str):
        name, code = cls.__ip_to_country__ip_api(ip)
        obj, _ = Country.objects.get_or_create(name=name, code=code)
        return obj

    @staticmethod
    def countries_for_url(url: Url):
        return {v.country for v in Visitor.objects.filter(url=url).only("country")}


class Visitor(Model):
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

    url = ForeignKey(to=Url, on_delete=SET_NULL, null=True)
    country = ForeignKey(to=Country, on_delete=DO_NOTHING, to_field="name", default="-")

    date = DateField(auto_now_add=True)
    hour = IntegerField(choices=TIME_FRAMES, help_text="Stores the visit time in 2-hour timeframes")

    number = IntegerField(default=0)

    class Meta:
        ordering = ["-date", "url", "-number"]
        get_latest_by = "date"

    def __str__(self):  # e.g: "/url (47) 'Italy'"
        return f"[{self.date}] {self.url} ({self.number}) '{self.country}'"

    def clean(self):
        self.hour = Visitor.__time_to_timeframe_key()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @staticmethod
    def for_url_from_country(url: Url, country: Country):
        """Gives the number of visitors for a specific Url and Country"""
        numbers = [v.number for v in Visitor.objects.filter(url=url, country=country).only("number")]
        return sum(numbers)

    @staticmethod
    def for_url_countriely(url: Url):
        """Gives the categorized number of visitors to a specific URL of the available Country(s)"""
        data = {}
        countries = Country.countries_for_url(url=url)
        for country in countries:
            data[country] = Visitor.for_url_from_country(url=url, country=country)
        return data

    @staticmethod
    def for_url_from_country_hourly(url: Url, country: Country):
        """Gives a categorized number of visitors, grouped by hour, for a specific URL and Country"""
        data = {}
        for k, tf in Visitor.TIME_FRAMES:
            qs = Visitor.objects.filter(url=url, country=country, hour=k).only("number")
            data[f"{tf}"] = sum([v.count for v in qs])
        return data

    @staticmethod
    def for_url_countriely_hourly(url: Url):
        """Gives a categorized number of visitors grouped by hour for a specific URL from all available Country(s)"""
        data = {}
        countries = Country.countries_for_url(url=url)
        for country in countries:
            data[f"{country}"] = Visitor.for_url_from_country_hourly(url=url, country=country)
        return data

    @staticmethod
    def for_url_most_country(url: Url):
        country_number = sorted(
            Visitor.for_url_countriely(url=url).items(),
            key=lambda x: x[1],
            reverse=True,
        )[0]
        return country_number[0]

    @staticmethod
    def for_url_least_country(url: Url):
        country_number = sorted(
            Visitor.for_url_countriely(url=url).items(),
            key=lambda x: x[1],
        )[0]
        return country_number[0]

    @staticmethod
    def increase_or_create(url: Url = None, country: Country = None):
        obj, _ = Visitor.objects.get_or_create(
            url=url,
            country=country,
            date=timezone.now(),
            hour=Visitor.__time_to_timeframe_key(),
        )
        obj.number += 1
        obj.save()

    @staticmethod
    def __time_to_timeframe_key():
        """Converts the current time to the "TIME FRAMES" key"""
        return timezone.now().hour // 2 * 2
