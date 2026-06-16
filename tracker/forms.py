from django import forms
from django_filters import FilterSet, ChoiceFilter
from .models import Wydatek, Przychod, Cel, KATEGORIE

class WydatekForm(forms.ModelForm):
    class Meta:
        model = Wydatek
        fields = ['nazwa', 'kwota', 'kategoria', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

class PrzychodzForm(forms.ModelForm):
    class Meta:
        model = Przychod
        fields = ['opis', 'kwota', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

class CelForm(forms.ModelForm):
    class Meta:
        model = Cel
        fields = ['nazwa', 'kwota_docelowa', 'kwota_odlozona', 'termin']
        widgets = {
            'termin': forms.DateInput(attrs={'type': 'date'}),
        }

class WydatekFilter(FilterSet):
    kategoria = ChoiceFilter(choices=[('', 'Wszystkie')] + KATEGORIE)

    class Meta:
        model = Wydatek
        fields = ['kategoria']