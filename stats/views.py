from django.shortcuts import render
from django.db.models import Count

from .utils import user_is_superuser

from promotions.models import Professor, Student, Lesson
from skills.models import Skill, KhanAcademyVideoSkill, SesamathSkill


@user_is_superuser
def dashboard(request):
    return render(request, "stats/dashboard.haml", {
        "professors": Professor.objects.all(),
        "students": Student.objects.all(),
        "lessons": Lesson.objects.all(),
        "skills": Skill.objects.all(),
        "skills_with_khan_ressources": Skill.objects.annotate(Count('khanacademyvideoskill')).filter(khanacademyvideoskill__count__gt=0),
        "skills_with_sesamath_ressources": Skill.objects.annotate(Count('sesamathskill')).filter(sesamathskill__count__gt=0),
        "khanacademyvideoskill": KhanAcademyVideoSkill.objects.order_by('-created_at'),
        "sesamathskill": SesamathSkill.objects.order_by('-created_at'),
    })
