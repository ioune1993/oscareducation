# encoding: utf-8

from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from skills.models import VideoSkill, ExternalLinkSkill, ExerciceSkill, KhanAcademyVideoReference
from examinations.models import BaseTest

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

    def get_or_generate_email(self, username):
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
        model = BaseTest
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


class KhanAcademyVideoReferenceForm(forms.Form):
    url = forms.URLField()

    def clean_url(self):
        data = self.cleaned_data["url"]

        slug = filter(None, data.split("/"))[-1]

        try:
            self.reference = KhanAcademyVideoReference.objects.get(slug=slug)
        except KhanAcademyVideoReference.DoesNotExist:
            raise forms.ValidationError(('Impossible de trouver la vidéo à cette page'), code='invalide')

        return data


class SesamathReferenceForm(forms.Form):
    ref_pk = forms.IntegerField()


class SyntheseForm(forms.Form):
    synthese = forms.CharField()
