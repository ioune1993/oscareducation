from django.views.generic import DetailView, UpdateView
from django.shortcuts import get_object_or_404

from .models import Lesson, Student


class LessonMixin(object):
    def get_context_data(self, **kwargs):
        context = super(LessonMixin, self).get_context_data(**kwargs)

        context["lesson"] = get_object_or_404(Lesson, pk=self.kwargs["lesson_pk"])

        # TODO check professor can only see a student in his lesson

        return context


class LessonStudentListView(DetailView):
    model = Lesson
    template_name = "professor/lesson/student/list.haml"
    context_object_name = "lesson"


class LessonStudentUpdateView(LessonMixin, UpdateView):
    model = Student
    template_name = "professor/lesson/student/update.haml"
    fields = ('user',)
