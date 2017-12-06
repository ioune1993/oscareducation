import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oscar.settings")
django.setup()
import factory
from promotions.models import Lesson


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lesson
        django_get_or_create = ('id', 'name', 'stage_id')

    @factory.post_generation
    def students(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for student in extracted:
                self.students.add(student)

    @factory.post_generation
    def professors(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for professor in extracted:
                self.professors.add(professor)
