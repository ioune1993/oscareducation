# encoding: utf-8

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import InlineRadios, InlineField

from .models import StudentPoll


class StudentYearField(InlineField):
    template = "%s/layout/student_year_field.html"


class StudentPollForm(forms.ModelForm):
    """A poll to fill to give feedback on Oscar.

    This is the poll that students are invited to complete each time
    they finish a test. The purpose is to get a feedback on Oscar
    from the students.
    """
    easy_to_connect_and_understand = forms.TypedChoiceField(
        required=True,
        label=u"Tu t'es facilement connecté·e à Oscar et tu as tout de suite compris ce qu'il fallait faire :",
        choices=tuple([(x, str(x)) for x in range(0, 4)]),
        widget=forms.RadioSelect,
    )

    enjoyed_oscar = forms.TypedChoiceField(
        required=True,
        label=u"As-tu aimé utiliser Oscar ?",
        choices=tuple([(x, str(x)) for x in range(0, 4)]),
        widget=forms.RadioSelect,
    )

    my_teacher_should_use_oscar_more = forms.TypedChoiceField(
        required=True,
        label=u"Aimerais-tu que ton enseignant·e travaille plus souvent avec Oscar ?",
        choices=((1, "Oui"), (0, "Non")),
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        super(StudentPollForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                StudentYearField("student_age"),

                "where",
                "on_device",

                InlineRadios("easy_to_connect_and_understand"),
                HTML(u'<div class="inline-radio-description"><span class="left">(non, c\'est compliqué)</span> <span class="right">(oui, c\'était très facile)</span></div>'),

                "difficulties",

                # "is_oscar_useful",

                # InlineRadios("saw_the_updated_skills_after_test"),

                # HTML(u"Si oui, tu as compris que :"),
                # InlineField("meaning_orange_circles"),
                # InlineField("meaning_green_circles"),
                # InlineField("meaning_white_circles"),

                # HTML(u"Tu as vu que tes compétences étaient mises à jour et..."),
                # "update_skills_motivated_me",
                # "update_skills_i_understood",
                # "update_skills_i_havent_understood",
                # "update_skills_havent_saw_it",
                # InlineField("update_skills_other"),

                InlineRadios("enjoyed_oscar", css_class="center-radio"),
                HTML(u'<div class="inline-radio-description"><span class="left">(non pas du tout)</span> <span class="right">(oui, c\'était génial !)</span></div>'),

                "why",

                InlineRadios("my_teacher_should_use_oscar_more"),
            ),
            ButtonHolder(
                Submit('submit', 'Valider', css_class='btn btn-primary')
            )
        )

    class Meta:
        model = StudentPoll
        exclude = ('student', 'lesson')
        widgets = {
            'on_device': forms.RadioSelect,
            'where': forms.RadioSelect,
            'meaning_orange_circles': forms.TextInput,
            'meaning_green_circles': forms.TextInput,
            'meaning_white_circles': forms.TextInput,
            'update_skills_other': forms.TextInput,
        }
