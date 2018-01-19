from django import forms
from .models import Scenario

class ScenarioForm(forms.Form):
    # TODO foreignkey
    creator = forms.CharField()
    title = forms.CharField() #("Titre", max_length = 255)
    skill = forms.CharField()
    topic = forms.CharField()
    grade_level = forms.CharField()
    instructions = forms.CharField() # ("Instructions", max_length = 755)
    public = forms.BooleanField()
    backgroundImage = forms.CharField()
