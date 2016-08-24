from django import template
from skills.models import StudentSkill


register = template.Library()

@register.simple_tag(takes_context=True)
def get_students_skills(context, of_keyword, student, at_keyword, stage, as_keyword, target_name):
    context[target_name] = StudentSkill.objects.filter(skill__in=stage.skills.all(), student=student).select_related("skill").order_by("skill__section", "skill__code")
    return ""
