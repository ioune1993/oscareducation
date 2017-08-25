# encoding: utf-8

from django import forms
from django.contrib.auth.models import User
from users.models import Professor,Student
from datetime import datetime, timedelta
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify


class UsernameLoginForm(forms.Form):
    username = forms.CharField(max_length=120)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except:
            raise forms.ValidationError("This user does not exist.")

        try:
            prof_or_stud = Professor.objects.get(user=user)
        except:
            try:
                prof_or_stud = Student.objects.get(user=user)
            except:
                raise forms.ValidationError("This user is not a student nor a professor.")

        return (prof_or_stud,username)

class CodeForm(UsernameLoginForm):
    code = forms.CharField(max_length=4)

    def clean(self):
        cleaned_data = super(CodeForm, self).clean()
        username = cleaned_data.get('username')
        code = cleaned_data.get('code')
        # Check if the code is correct
        if not username or not username[0].code == int(code):
            raise forms.ValidationError("This code is not correct.")
        # Check if the code is not expired
        dt = datetime.now() - username[0].code_created_at.replace(tzinfo=None) - timedelta(days=2)
        if dt > timedelta(hours=0):
            raise forms.ValidationError("This code has expired.")

        return cleaned_data

class CreatePasswordForm(UsernameLoginForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirmed_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(CreatePasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirmed_password = cleaned_data.get('confirmed_password')
        if not password == confirmed_password:
            raise forms.ValidationError("The given password are not the same.")

        return cleaned_data

class SubscribeTeacherForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    registration_number_validator = RegexValidator(r'^(0|1|2){1}(\d{2})(\d{2})(\d{2})(\d{4})', "Le matricule donné n'est pas valide.")
    registration_number = forms.CharField(validators=[registration_number_validator])

    def generate_teacher_username(self):
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
            raise forms.ValidationError("Email manquant.")
        if User.objects.filter(email=self.cleaned_data["email"]):
            raise forms.ValidationError("Cette adresse email est déjà utilisée par un autre utilisateur.")

        return self.cleaned_data["email"]

    def clean_first_name(self):
        if not self.cleaned_data["first_name"]:
            raise forms.ValidationError("Prénom manquant.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if not self.cleaned_data["last_name"]:
            raise forms.ValidationError("Nom de famille manquant.")
        return self.cleaned_data["last_name"]

    def clean_password(self):
        if not self.cleaned_data["password"]:
            raise forms.ValidationError("Mot de passe manquant.")
        return self.cleaned_data["password"]
