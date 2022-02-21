from .Init import *


class CreatorModelTest(Init):
    def test__Free_Accounts__different_url_creations(self):
        self.creator.set_to_Free_Account()

        for _ in range(Creator.Account.Free.max_url_a_day):
            self.make_url(save=True)

        self.assertEqual(self.creator.can_generate_url_tody, False)
        self.assertEqual(self.creator.can_generate_monitored_url, False)
        self.assertEqual(self.creator.can_generate_url, True)

    def test__Advanced_Accounts__different_url_creations(self):
        self.creator.set_to_Advanced_Account()

        for _ in range(Creator.Account.Advanced.max_url_a_day):
            self.make_url(save=True)

        self.assertEqual(self.creator.can_generate_url_tody, False)
        self.assertEqual(self.creator.can_generate_monitored_url, True)
        self.assertEqual(self.creator.can_generate_url, True)

    def test__Complete_Accounts__different_url_creations(self):
        self.creator.set_to_Complete_Account()

        for _ in range(Creator.Account.Complete.max_url_a_day):
            self.make_url(save=True)

        self.assertEqual(self.creator.can_generate_url_tody, False)
        self.assertEqual(self.creator.can_generate_monitored_url, True)
        self.assertEqual(self.creator.can_generate_url, True)

    def test__switching_between_account_types(self):
        self.creator.set_to_Free_Account()
        self.assertEqual(self.creator.account_type, Creator.Account.Types.FREE)
        self.assertEqual(self.creator.max_url, Creator.Account.Free.max_url)
        self.assertEqual(self.creator.max_url_a_day, Creator.Account.Free.max_url_a_day)
        self.assertEqual(self.creator.max_monitored_url, Creator.Account.Free.max_monitored_url)
        self.assertEqual(self.creator.type, "Free")

        self.creator.set_to_Advanced_Account()
        self.assertEqual(self.creator.account_type, Creator.Account.Types.ADVANCED)
        self.assertEqual(self.creator.max_url, Creator.Account.Advanced.max_url)
        self.assertEqual(self.creator.max_url_a_day, Creator.Account.Advanced.max_url_a_day)
        self.assertEqual(self.creator.max_monitored_url, Creator.Account.Advanced.max_monitored_url)
        self.assertEqual(self.creator.type, "Advanced")

        self.creator.set_to_Complete_Account()
        self.assertEqual(self.creator.account_type, Creator.Account.Types.COMPLETE)
        self.assertEqual(self.creator.max_url, Creator.Account.Complete.max_url)
        self.assertEqual(self.creator.max_url_a_day, Creator.Account.Complete.max_url_a_day)
        self.assertEqual(self.creator.max_monitored_url, Creator.Account.Complete.max_monitored_url)
        self.assertEqual(self.creator.type, "Complete")
