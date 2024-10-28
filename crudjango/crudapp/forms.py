from django import forms
from .models import Persons

class PersonForm(forms.ModelForm):
    class Meta:
        model = Persons
        fields = ['fname', 'lname', 'age', 'email', 'city']
