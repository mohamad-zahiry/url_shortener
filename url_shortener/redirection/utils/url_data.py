from django.utils import timezone

from redirection.models import UrlData, now_timeframe, Country


def increase_visits_or_create(key, country=None):
    if not country:
        country = Country.objects.get_or_create(name="")[0]

    obj, _ = UrlData.objects.get_or_create(
        key=key,
        country=country,
        hour=now_timeframe(),
        date=timezone.now(),
    )
    obj.visits += 1
    obj.save()
