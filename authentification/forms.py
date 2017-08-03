from django import forms
from django.contrib.auth.models import User
from users.models import Professor,Student
from datetime import datetime, timedelta

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
        print(datetime.now())
        print(username[0].code_created_at)
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