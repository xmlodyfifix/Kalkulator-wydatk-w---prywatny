from django import forms
from django_filters import FilterSet, ChoiceFilter
from .models import Wydatek, KATEGORIE

class WydatekForm(forms.ModelForm):
    class Meta:
        model = Wydatek
        fields = ['nazwa', 'kwota', 'kategoria', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

class WydatekFilter(FilterSet):
    kategoria = ChoiceFilter(choices=[('', 'Wszystkie')] + KATEGORIE)

    class Meta:
        model = Wydatek
        fields = ['kategoria']