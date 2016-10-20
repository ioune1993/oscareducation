from django.test import TestCase, Client


class PermissionsTest(TestCase):
    def test_unlogged_go_to_homepage(self):
        c = Client()

        response = c.get("/")
        assert response.url == 'http://testserver/accounts/login/'
        assert response.status_code == 302
