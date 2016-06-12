from django import forms

from .models import VideoSkill


class VideoSkillForm(forms.Form):
    class Meta:
        model = VideoSkill
