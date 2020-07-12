from django.test import TestCase
from dashboard.views import signup, activate

class TestViews(TestBase):

    def setUp(self):
        super().setUp()

    # TODO: test view functions signup
    def test_signup():
        assert True == True

    # TODO: test view functions activate
    def test_activate():
        assert True == True

    # TODO: test axes account lockout
    def test_user_lockout():
