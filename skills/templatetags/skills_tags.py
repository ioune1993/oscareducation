from django import template
register = template.Library()

@register.filter
def splitcode(skill):
    return skill.code.split("-")[2]
