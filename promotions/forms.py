# encoding: utf-8

from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from skills.models import VideoSkill, ExternalLinkSkill, ExerciceSkill, KhanAcademyVideoSkill
from examinations.models import Test

from .models import Lesson


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'stage']


class LessonUpdateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name']


class StudentAddForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(required=False)

    def generate_student_username(self):
        username = slugify(self.cleaned_data["first_name"]) + "." + slugify(self.cleaned_data["last_name"])

        # handle duplicated usernames
        # not optimised at all
        base_username = username

        number = 1
        while User.objects.filter(username=username):
            username = base_username + str(number)
            number += 1

        return username

    def clean_email(self):
        if not self.cleaned_data["email"]:
            return

        if User.objects.filter(email=self.cleaned_data["email"]):
            raise forms.ValidationError("Cette adresse email est déjà utilisé par un autre utilisateur")

        return self.cleaned_data["email"]

    def generate_email(self, username):
        if self.cleaned_data["email"]:
            return self.cleaned_data["email"]

        # hack, django enforce an email usage, let's use @example.com for "I don't have an email"
        return username + "@example.com"


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class TestUpdateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name']


class VideoSkillForm(forms.ModelForm):
    class Meta:
        model = VideoSkill
        fields = ['skill', 'title', 'duration', 'difficulty', 'url']


class ExerciceSkillForm(forms.ModelForm):
    class Meta:
        model = ExerciceSkill
        fields = ['skill', 'title', 'duration', 'difficulty', 'questions', 'answers']


class ExternalLinkSkillForm(forms.ModelForm):
    class Meta:
        model = ExternalLinkSkill
        fields = ['skill', 'title', 'duration', 'difficulty', 'url']


class KhanAcademyVideoSkillForm(forms.ModelForm):
    class Meta:
        model = KhanAcademyVideoSkill
        fields = ['skill', 'url', 'youtube_id']


class SyntheseForm(forms.Form):
    synthese = forms.CharField()
