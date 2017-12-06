from django.test import TestCase, RequestFactory
from questions_factory.views import *


class ProblemGenerationRequests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_put_request_on_generator_submit_no_user(self):
        # Access must fail because of user_is_professor
        with self.assertRaises(AttributeError):
            request = self.factory.put('/questions_factory/generator/272727/88/9022772/')
            generator_submit(request, 222, 222, 222)

