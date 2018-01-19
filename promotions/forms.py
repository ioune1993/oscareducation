# encoding: utf-8

from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from resources.models import KhanAcademy, Sesamath, Resource
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

    def clean_first_name(self):
        if not self.cleaned_data["first_name"]:
            raise forms.ValidationError("Prénom manquant.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if not self.cleaned_data["last_name"]:
            raise forms.ValidationError("Nom de famille manquant.")
        return self.cleaned_data["last_name"]

    def get_or_generate_email(self, username):
        if self.cleaned_data["email"]:
            return self.cleaned_data["email"]

        # hack, django enforce an email usage, let's use @example.com for "I don't have an email"
        return username + "@example.com"

def validate_file_extension(value):
    if not value.name.endswith('.xls'):
        raise forms.ValidationError("Only XLS file is accepted")

class CSVForm(forms.Form):
    csvfile = forms.FileField(validators=[validate_file_extension])

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class TestUpdateForm(forms.ModelForm):
    class Meta:
        model = BaseTest
        fields = ['name']


class KhanAcademyForm(forms.Form):

    #url = forms.URLField()
    url = forms.CharField(required=False, label="Nom")
    """
    def clean_url(self):
        data = self.cleaned_data["url"].split("?")[0]

        slug = filter(None, data.split("/"))[-1]

        try:
            self.reference = KhanAcademy.objects.get(slug=slug)
        except KhanAcademy.DoesNotExist:
            raise forms.ValidationError(('Impossible de trouver la vidéo à cette page'), code='invalide')

        return data"""


class SesamathForm(forms.Form):
    ref_pk = forms.IntegerField()


class SyntheseForm(forms.Form):
    synthese = forms.CharField()


class ResourceForm(forms.ModelForm):
    """ Resource form """
    kind = forms.ChoiceField(required=True, label="Genre",choices=(
        ("practical-application", "Application pratique"),
        ("lesson", "Cours"),
        ("exercice", "Exercices"),
        ("commented-exercice", "Exercices commentés"),
        ("exercice-correction", "Correction d´exercices"),
        ("learning-sequence", "Séquence d´apprentissage"),
        ("synthesis", "Synthèse"),
        ("reference", "Référence (presse, histoire)"),
        ("other", "(autre)"),
    ))

    type = forms.ChoiceField(required=True, label="Type", choices=(
        ("animation", "Animation"),
        ("software", "Application (ordinateur)"),
        ("mobile-app", "Application mobile"),
        ("document", "Document"),
        ("image", "Image"),
        ("game", "Jeu"),
        ("tool", "Outil"),
        ("project", "Projet / énigme"),
        ("synthesis", "Synthèse"),
        ("site", "Site"),
        ("test", "Test"),
        ("video", "vidéo"),
        ("other", "autre"),
    ))

    name = forms.CharField(required=False, label="Nom")

    text = forms.CharField(required=False, label="Commentaire", widget=forms.Textarea)

    link = forms.URLField(required=False, label="Lien")

    file = forms.FileField(required=False,label="Fichier")


    class Meta:
        model = Resource
        fields = ('content', 'added_by', 'section')
