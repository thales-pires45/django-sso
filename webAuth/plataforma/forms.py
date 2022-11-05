from django import forms
from django.forms.fields import CharField, EmailField, IntegerField

class FormTeste(forms.Form):
    nome = CharField(max_length=20)
    email = EmailField()
    id = IntegerField()
    