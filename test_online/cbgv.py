from django.views.generic import DetailView

from examinations.models import Test

from promotions.cbgv import LessonMixin


class TestDetailView(LessonMixin, DetailView):
    model = Test
    template_name = "professor/lesson/test/online/detail.haml"
