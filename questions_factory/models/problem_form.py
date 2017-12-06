# coding=utf-8
from django import forms


class GeneratorChoiceForm(forms.Form):
    GENERATOR_CHOICE = (("ArithmeticProblem", "Equation du second degrée"),
                        ("SimpleInterestProblem", "Problèmes d'intêret"),
                        ("StatisticsProblem", "Problèmes de statistiques"),
                        ("VolumeProblem", "Problèmes de volume"),
                        ("PerimeterProblem", "Problèmes de périmètre"),
                        ("AreaProblem", "Problèmes d'aire"),
                        ("PythagorasProblem", "Théorème de Pythagore"))

    LIST_NAME_FIELD = ["generator_name", "nb_question", "nb_decimal"]

    generator_name = forms.ChoiceField(widget=forms.Select, choices=GENERATOR_CHOICE, label='Problème à générer')
    nb_question = forms.FloatField(widget=forms.TextInput, required=True, initial=5,
                                   label='Nombre de questions')
    nb_decimal = forms.FloatField(widget=forms.TextInput, required=True, initial=2,
                                  label='Nombre de décimales')

    def clean(self):
        cleaned_data = super(GeneratorChoiceForm, self).clean()
        nb_question = cleaned_data.get("nb_question")
        nb_decimal = cleaned_data.get("nb_decimal")
        if nb_question < 1 or nb_question > 50:
            msg = "Le nombre de questions générées doit être compris entre 1 et 50"
            self.add_error('nb_question', msg)
        if nb_decimal < 1 or nb_decimal > 8:
            msg = "Le nombre de décimales générées doit être compris entre 1 et 8"
            self.add_error('nb_question', msg)
        return cleaned_data


class ArithmeticForm(GeneratorChoiceForm):
    DOMAIN_CHOICES = (('Integer', 'Entiers'), ('Rational', 'Rationnels'))
    IMAGE_CHOICES = (('Rational', 'Rationnels'), ('Complex', 'Complexes'), ('Integer', 'Entiers'))

    range_from = forms.FloatField(widget=forms.TextInput, required=True, label='Intervalle inférieur')
    range_to = forms.FloatField(widget=forms.TextInput, required=True, label='Intervalle supérieur')
    domain = forms.ChoiceField(widget=forms.Select, choices=DOMAIN_CHOICES, label='Domaine')
    image = forms.ChoiceField(widget=forms.Select, choices=IMAGE_CHOICES, label='Image')

    def clean(self):
        cleaned_data = super(ArithmeticForm, self).clean()
        range_from = cleaned_data.get("range_from")
        range_to = cleaned_data.get("range_to")

        # Checking instance to avoid problem with 0 values
        if isinstance(range_from, float) and isinstance(range_to, float):
            if range_from >= range_to:
                msg = "L'intervalle inférieur ne peut pas être plus grand ou égal à l'intervalle supérieur."
                self.add_error('range_from', msg)
            if (range_to - range_from) < 5:
                msg = "Fournissez un intervalle de valeur supérieur ou égal à 5"
                self.add_error('range_from', msg)


class SimpleInterestForm(GeneratorChoiceForm):
    TIME_CHOICES = (('year', 'Années'), ('month', 'Mois'))

    time_placed = forms.ChoiceField(widget=forms.Select, choices=TIME_CHOICES, label='Temps de placement')
    type_rate = forms.ChoiceField(widget=forms.Select, choices=TIME_CHOICES, label='Ratio appliqué par')


class StatisticsForm(GeneratorChoiceForm):
    range_from = forms.FloatField(widget=forms.TextInput, required=True, label='Intervalle inférieur des valeurs')
    range_to = forms.FloatField(widget=forms.TextInput, required=True, label='Intervalle supérieur des valeurs')
    nb = forms.IntegerField(widget=forms.TextInput, required=True, label='Nombre d''éléments')

    def clean(self):
        cleaned_data = super(StatisticsForm, self).clean()
        range_from = cleaned_data.get("range_from")
        range_to = cleaned_data.get("range_to")
        nb = cleaned_data.get("nb")
        if isinstance(range_from, float) and isinstance(range_to, float) and isinstance(nb, int):
            if range_from >= range_to:
                msg = "L'intervalle inférieur ne peut pas être plus grand ou égal à l'intervalle supérieur."
                self.add_error('range_from', msg)
            if (range_to - range_from) < 1:
                msg = "Fournissez un intervalle de valeur supérieur ou égal à 1"
                self.add_error('range_from', msg)
            if nb < 5:
                msg = "Le nombre d'éléments doit être au minimum de 5"
                self.add_error('nb', msg)


class VolumeProblemForm(GeneratorChoiceForm):
    OBJECT_TYPE = (('cylinder', 'Cylindre'),
                   ('pyramid', 'Pyramide'),
                   ('cone', 'Cône'),
                   ('prism', 'Prisme'),
                   ('cube', 'Cube'))

    object_type = forms.ChoiceField(widget=forms.Select, choices=OBJECT_TYPE, label='Figure')
    range_from = forms.FloatField(widget=forms.TextInput, required=True, label='Intervalle inférieur')
    range_to = forms.FloatField(widget=forms.TextInput, required=True, label='Intervalle supérieur')

    def clean(self):
        cleaned_data = super(VolumeProblemForm, self).clean()
        range_from = cleaned_data.get("range_from")
        range_to = cleaned_data.get("range_to")
        if isinstance(range_from, float) and isinstance(range_to, float):
            if range_from <= 0 or range_to <= 0:
                msg = "Les valeurs doivent être plus grandes que 0."
                self.add_error('range_from', msg)
            if range_from >= range_to:
                msg = "L'intervalle inférieur ne peut pas être plus grand ou égal à l'intervalle supérieur."
                self.add_error('range_from', msg)
            if (range_to - range_from) < 1:
                msg = "Fournissez un intervalle de valeurs supérieur ou égal à 1"
                self.add_error('range_from', msg)


class PerimeterProblemForm(GeneratorChoiceForm):
    OBJECT_TYPE = (('rhombus', 'Losange'),
                   ('rectangle', 'Rectangle'),
                   ('square', ' Carré'),
                   ('triangle', 'Triangle'),
                   ('trapezium', 'Trapèze'),
                   ('quadrilateral', 'Quadrilatère'),
                   ('circle', 'Cercle'),
                   ('parallelogram', 'Parralélogramme'),
                   ('regular_polygon', 'Polygone régulier')
                   )

    object_type = forms.ChoiceField(widget=forms.Select, choices=OBJECT_TYPE, label='Figure')
    range_from = forms.FloatField(widget=forms.TextInput, required=True, label='Intervalle inférieur')
    range_to = forms.FloatField(widget=forms.TextInput, required=True, label='Intervalle supérieur')

    def clean(self):
        cleaned_data = super(PerimeterProblemForm, self).clean()
        range_from = cleaned_data.get("range_from")
        range_to = cleaned_data.get("range_to")
        if isinstance(range_from, float) and isinstance(range_to, float):
            if range_from <= 0 or range_to <= 0:
                msg = "Les valeurs doivent être plus grandes que 0."
                self.add_error('range_from', msg)
            if range_from >= range_to:
                msg = "L'intervalle inférieur ne peut pas être plus grand ou égal au supérieur."
                self.add_error('range_from', msg)
            if (range_to - range_from) < 1:
                msg = "Fournissez un intervalle de valeurs supérieur ou égal à 1"
                self.add_error('range_from', msg)


class AreaProblemForm(GeneratorChoiceForm):
    OBJECT_TYPE = (('rhombus', 'Losange'),
                   ('rectangle', 'Rectangle'),
                   ('square', ' Carré'),
                   ('triangle', 'Triangle'),
                   ('trapezium', 'Trapèze'),
                   ('quadrilateral', 'Quadrilatère'),
                   ('circle', 'Cercle'),
                   ('parallelogram', 'Parralélogramme'),
                   ('regular_polygon', 'Polygone régulier')
                   )

    object_type = forms.ChoiceField(widget=forms.Select, choices=OBJECT_TYPE, label='Figure')
    range_from = forms.FloatField(widget=forms.TextInput, required=True, label='Intervalle inférieur')
    range_to = forms.FloatField(widget=forms.TextInput, required=True, label='Intervalle supérieur')

    def clean(self):
        cleaned_data = super(AreaProblemForm, self).clean()
        range_from = cleaned_data.get("range_from")
        range_to = cleaned_data.get("range_to")
        if isinstance(range_from, float) and isinstance(range_to, float):
            if range_from <= 0 or range_to <= 0:
                msg = "Les valeurs doivent être plus grandes que 0."
                self.add_error('range_from', msg)
            if range_from >= range_to:
                msg = "L'intervalle inférieur ne peut pas être plus grand ou égal au supérieur."
                self.add_error('range_from', msg)
            if (range_to - range_from) < 1:
                msg = "Fournissez un intervalle de valeurs supérieur ou égal à 1"
                self.add_error('range_from', msg)


class PythagorasProblemForm(GeneratorChoiceForm):
    range_from = forms.FloatField(widget=forms.TextInput, required=True, label='Intervalle inférieur')
    range_to = forms.FloatField(widget=forms.TextInput, required=True, label='Intervalle supérieur')

    def clean(self):
        cleaned_data = super(PythagorasProblemForm, self).clean()
        range_from = cleaned_data.get("range_from")
        range_to = cleaned_data.get("range_to")
        if isinstance(range_from, float) and isinstance(range_to, float):
            if range_from <= 0 or range_to <= 0:
                msg = "Les valeurs doivent être plus grandes que 0."
                self.add_error('range_from', msg)
            if range_from >= range_to:
                msg = "L'intervalle inférieur ne peut pas être plus grand ou égal à l'intervalle supérieur."
                self.add_error('range_from', msg)
            if (range_to - range_from) < 1:
                msg = "Fournissez un intervalle de valeurs supérieur ou égal à 1"
                self.add_error('range_from', msg)
