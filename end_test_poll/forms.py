# encoding: utf-8

from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import InlineRadios, InlineField

from .models import StudentPoll


class SwappedInlineField(InlineField):
    template = "%s/layout/swapped_inline_field.html"


class StudentPollForm(forms.ModelForm):
    easy_to_connect_and_understand = forms.TypedChoiceField(
        required=True,
        label=u"Je me suis facilement connecté·e à Oscar et j'ai tout de suite compris ce qu'il fallaire faire :",
        choices=tuple([(x, str(x)) for x in range(1, 5)]),
        widget=forms.RadioSelect,
    )

    enjoyed_oscar = forms.TypedChoiceField(
        required=True,
        label=u"As-tu aimé utiliser Oscar ?",
        choices=tuple([(x, str(x)) for x in range(1, 5)]),
        widget=forms.RadioSelect,
    )

    my_teacher_should_use_oscar_more = forms.TypedChoiceField(
        required=True,
        label=u"Aimerais-tu que ton enseignant·e travaille plus souvent avec Oscar ?",
        choices=((True, "Oui"), (False, "Non")),
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        super(StudentPollForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                InlineField("student_age"),

                HTML(u"<p>Depuis mi-avril, je me suis connecté·e :</p>"),
                SwappedInlineField("at_school_on_computer", style="width: 70px;"),
                SwappedInlineField("at_school_on_tablette", style="width: 70px;"),
                SwappedInlineField("at_school_on_smartphone", style="width: 70px;"),

                SwappedInlineField("at_home_on_computer", style="width: 70px;"),
                SwappedInlineField("at_home_on_tablette", style="width: 70px;"),
                SwappedInlineField("at_home_on_smartphone", style="width: 70px;"),

                SwappedInlineField("on_smartphone_somewhere_else", style="width: 70px;"),

                InlineRadios("easy_to_connect_and_understand"),
                HTML(u'<div class="inline-radio-description"><span class="left">(oui, c\'était très facile)</span> <span class="right">(non, c\'est compliqué)</span></div>'),

                "difficulties",

                InlineRadios("my_teacher_should_use_oscar_more"),

                # "is_oscar_usefull",

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

                InlineRadios("enjoyed_oscar"),
                HTML(u'<div class="inline-radio-description"><span class="left">(non pas du tout)</span> <span class="right">(oui, c\'était génial !)</span></div>'),

                "why",

                "what_on_oscar_to_better_learn_math",
            ),
            ButtonHolder(
                Submit('submit', 'Valider', css_class='btn btn-primary')
            )
        )

    class Meta:
        model = StudentPoll
        exclude = ('student',)
        widgets = {
            'meaning_orange_circles': forms.TextInput,
            'meaning_green_circles': forms.TextInput,
            'meaning_white_circles': forms.TextInput,
            'update_skills_other': forms.TextInput,
        }
