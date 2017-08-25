from django.core.urlresolvers import reverse
from django.views.generic import DetailView, DeleteView
from django.shortcuts import get_object_or_404

from .models import Lesson
from users.models import Student
from examinations.models import BaseTest


class LessonMixin(object):
    def get_lesson(self):
        return get_object_or_404(Lesson, pk=self.kwargs["lesson_pk"])

    def get_context_data(self, **kwargs):
        context = super(LessonMixin, self).get_context_data(**kwargs)

        context["lesson"] = self.get_lesson()

        # TODO check professor can only see a student in his lesson

        return context


class LessonStudentListView(DetailView):
    model = Lesson
    template_name = "professor/lesson/student/list.haml"
    context_object_name = "lesson"


class StudentDelete(LessonMixin, DeleteView):
    model = Student
    template_name = "professor/lesson/student/delete.haml"

    def get_success_url(self):
        return reverse('professor:lesson_detail', args=(self.get_lesson().pk,))


class LessonDelete(DeleteView):
    model = Lesson
    template_name = "professor/lesson/delete.haml"
    context_object_name = "lesson"

    def get_success_url(self):
        return reverse('professor:dashboard')


class BaseTestDelete(LessonMixin, DeleteView):
    model = BaseTest
    template_name = "professor/lesson/test/delete.haml"
    context_object_name = "test"

    def get_success_url(self):
        return reverse('professor:lesson_test_list', args=(self.get_lesson().pk,))
