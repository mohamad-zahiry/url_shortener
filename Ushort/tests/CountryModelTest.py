from .Init import *


class CountryModelTest(Init):
    def test__country_by_ip__with_invalid_ip(self):
        country = Country.country_by_ip("127.0.0.1")
        self.assertEqual((country.name, country.code), ("-", "-"))

    def test__country_by_ip__with_valid_ip(self):
        country = Country.country_by_ip("1.1.1.1")
        self.assertEqual((country.name, country.code), ("Australia", "AU"))

    def test__countries_for_url(self):
        url = self.make_url(save=True)
        countries = [
            Country.objects.create(name="Albania", code="AL"),
            Country.objects.create(name="Brazil", code="BR"),
            Country.objects.create(name="Denmark", code="DK"),
        ]

        for country in countries:
            Visitor.increase_or_create(url=url, country=country)

        self.assertEqual(Country.countries_for_url(url), set(countries))
