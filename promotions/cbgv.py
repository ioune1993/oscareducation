from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from .models import Lesson


class LessonMixin(object):
    def get_context_data(self, **kwargs):
        context = super(LessonMixin, self).get_context_data(**kwargs)

        context["lesson"] = get_object_or_404(Lesson, pk=kwargs["lesson_pk"])

        return context


class LessonStudentListView(DetailView):
    model = Lesson
    template_name = "professor/lesson/student/list.haml"
    context_object_name = "lesson"
