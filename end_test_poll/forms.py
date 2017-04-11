# encoding: utf-8

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML

from .models import StudentPoll


class StudentPollForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentPollForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                "student_age",

                HTML(u"<p>Depuis mi-avril, je me suis connecté·e :</p>"),
                "at_school_on_computer",
                "at_school_on_tablette",
                "at_school_on_smartphone",

                "at_home_on_computer",
                "at_home_on_tablette",
                "at_home_on_smartphone",

                "on_smartphone_somewhere_else",

                "easy_to_connect_and_understand",

                "difficulties",

                "enjoyed_oscar",

                "why",

                "my_teacher_should_use_oscar_more",

                "is_oscar_usefull",

                "saw_the_updated_skills_after_test",

                HTML(u"Si oui, tu as compris que :"),
                "meaning_orange_circles",
                "meaning_green_circles",
                "meaning_white_circles",

                HTML(u"Tu as vu que tes compétences étaient mises à jour et..."),
                "update_skills_motivated_me",
                "update_skills_i_understood",
                "update_skills_i_havent_understood",
                "update_skills_havent_saw_it",
                "update_skills_other",

                "what_on_oscar_to_better_learn_math",
            ),
            ButtonHolder(
                Submit('submit', 'Valider', css_class='btn btn-primary')
            )
        )

    class Meta:
        model = StudentPoll
        exclude = ('student',)
