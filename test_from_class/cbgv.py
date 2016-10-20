from django.views.generic import DetailView
from examinations.models import TestFromClass

from promotions.cbgv import LessonMixin


class TestFromClassDetailView(LessonMixin, DetailView):
    model = TestFromClass
    template_name = "professor/lesson/test/from-class/detail.haml"
