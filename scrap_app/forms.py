from django import forms
from .models import City, Language

class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all())
    lenguage = forms.ModelChoiceField(queryset=Language.objects.all())