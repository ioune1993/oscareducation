from django import template
from skills.models import StudentSkill
from promotions.models import Stage


register = template.Library()

@register.simple_tag(takes_context=True)
def get_students_skills(context, of_keyword, student, at_keyword, stage, as_keyword, target_name):
    context[target_name] = StudentSkill.objects.filter(skill__in=stage.skills.all(), student=student).select_related("skill").order_by("skill__section", "skill__code")
    return ""


@register.simple_tag
def get_skill_heatmap_class(skills_to_heatmap_class, skill):
    return skills_to_heatmap_class.get(skill, "")


@register.simple_tag
def get_stage_id(skill_short_name):
    return Stage.objects.get(short_name=skill_short_name).id
