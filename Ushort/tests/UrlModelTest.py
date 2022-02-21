from .Init import *


class UrlModelTests(Init):
    def test_expire_time_correctness(self):
        s = tz.now()  # access start
        d = tz.timedelta(days=5)  # access duration
        url = self.make_url(access_start=s, access_duration=d)
        self.assertEqual(url.expire_time, s + d)

    def test__is_stared__with_future_start_time(self):
        s = tz.now() + tz.timedelta(days=1)
        url = self.make_url(access_start=s)
        self.assertEqual(url.is_started, False)

    def test__is_stared__with_past_start_time(self):
        s = tz.now() + tz.timedelta(days=-1)
        url = self.make_url(access_start=s)
        self.assertEqual(url.is_started, True)

    def test__is_expired__with_past_expire_time(self):
        strt = tz.now() + tz.timedelta(days=-1)
        expr = tz.timedelta(hours=1)
        url = self.make_url(access_start=strt, access_duration=expr)
        self.assertEqual(url.is_expired, True)

    def test__is_expired__with_future_expire_time(self):
        strt = tz.now()
        expr = tz.timedelta(days=1)
        url = self.make_url(access_start=strt, access_duration=expr)
        self.assertEqual(url.is_expired, False)

    def test__expried_after__with_expired_url(self):
        strt = tz.now() + tz.timedelta(days=-1)
        expr = tz.timedelta()
        url = self.make_url(access_start=strt, access_duration=expr)
        self.assertEqual(url.expired_after, tz.timedelta())

    def test__expried_after__with_unexpired_url(self):
        strt = tz.now()
        expr = tz.timedelta(days=1)
        url = self.make_url(access_start=strt, access_duration=expr)
        # ? delta is used for fill the time gap between operations
        self.assertAlmostEqual(
            url.expired_after,
            url.expire_time - tz.now(),
            delta=tz.timedelta(minutes=1),
        )

    def test__expried_after__with_unstarted_url(self):
        strt = tz.now() + tz.timedelta(days=1)
        expr = tz.timedelta(days=1)
        url = self.make_url(access_start=strt, access_duration=expr)
        self.assertEqual(url.expired_after, expr)

    def test__is_public__with_access_code(self):
        url = self.make_url(access_code="secret")
        self.assertEqual(url.is_public, False)

    def test__is_public__without_access_code(self):
        url = self.make_url(access_code="")
        self.assertEqual(url.is_public, True)

    def test__check_access_code__with_correct_code(self):
        url = self.make_url(access_code="secret")
        self.assertEqual(url.check_access_code("secret"), True)

    def test__check_access_code__with_wrong_code(self):
        url = self.make_url(access_code="secret")
        self.assertEqual(url.check_access_code("wrongSecret"), False)

    def test_invalid_targets(self):
        url = self.make_url(target="invalid_url")
        self.assertRaises(ValidationError, url.save)

    def test__clean__with_a_not_permitted_creator_to_create_new_url(self):
        for _ in range(5):
            url = self.make_url(save=True, creator=self.creator)
        url = self.make_url()
        return self.assertRaises(ValidationError, url.clean)

    def test__clean__with_a_FreeAccount_creator_to_create_monitored_url(self):
        url = self.make_url(monitored=True)
        return self.assertRaises(ValidationError, url.clean)

    def test__clean__with_a_NonFreeAccount_creator_to_create_monitored_url(self):
        self.creator.set_to_Complete_Account()
        url = self.make_url(monitored=True)
        return self.assertEqual(url.clean(), None)

    def test__add_visitor__with_unmonitored_url(self):
        url = self.make_url(save=True)
        url.add_visitor(self.request_factory.get(f"/go2/{url.url}"))
        visitors = Url.objects.get(url=url.url).visitors
        self.assertEqual(visitors, 1)

    def test__add_visitor__with_unmonitored_expired_url(self):
        url = self.make_url(save=True, access_duration=tz.timedelta())
        url.add_visitor(self.request_factory.get(f"/go2/{url.url}"))
        url = Url.objects.get(url=url.url)
        self.assertEqual(url.visitors, 0)
        self.assertEqual(url.visitors_after_expire, 1)

    def test__add_visitor__with_monitored_url(self):
        self.creator.set_to_Advanced_Account()
        url = self.make_url(save=True, monitored=True)
        url.add_visitor(self.request_factory.get(f"/go2/{url.url}"))
        url = Url.objects.get(url=url.url)
        self.assertEqual(url.visitors, 1)

    def test__add_visitor__with_monitored_expired_url(self):
        self.creator.set_to_Advanced_Account()
        url = self.make_url(save=True, monitored=True, access_duration=tz.timedelta())
        req = self.request_factory.get(f"/go2/{url.url}")
        url.add_visitor(req)
        url = Url.objects.get(url=url.url)
        self.assertEqual(url.visitors, 0)
        self.assertEqual(url.visitors_after_expire, 1)
