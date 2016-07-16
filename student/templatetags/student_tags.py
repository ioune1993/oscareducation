from django import template

register = template.Library()

@register.filter
def keep_unfinished_tests(teststudent_set_all):
  return teststudent_set_all.filter(finished_at__isnull=True)

@register.filter
def strip_untested_skills(level_list):
  # filter (remove) untested skills
  filtered_level_list = []

  for student_skill in level_list:
    if student_skill.tested or student_skill.acquired:
      filtered_level_list.append(student_skill)

  return filtered_level_list
