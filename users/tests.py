# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase
from resources.models import *
from users.interface import Status
from users.models import Top_contributor
import json



class ProfessorTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(first_name="Bob",last_name="Fisher",username='Fishy')
        self.user2 = User.objects.create(first_name="Rick", last_name="Rocked", username='Stoned')
        self.prof1 = Professor.objects.create(
            status_changed=False,
            user=self.user1,
            nbr_4_star_res=0,
            is_pending=False
        )
        self.prof2 = Professor.objects.create(
            status_changed=False,
            user=self.user2,
            nbr_4_star_res=10,
            is_pending=False
        )

    def test_update_status(self):
        pass