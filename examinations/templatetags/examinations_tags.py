from django import template
register = template.Library()

@register.filter
def answer(List, i):
    return List[int(i)][0]

@register.filter
def is_correct(List,i):
    return List[int(i)][1]