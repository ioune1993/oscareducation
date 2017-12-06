import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oscar.settings")
django.setup()
import factory
from promotions.models import Stage


class StageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Stage
        django_get_or_create = ('id', 'name', 'short_name', 'level', 'previous_stage_id')

    @factory.post_generation
    def skills(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for skill in extracted:
                self.skills.add(skill)