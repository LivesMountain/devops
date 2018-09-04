from django import forms
# from .models import

class AddForm(forms.Form):
    Responsible = forms.CharField()
    Business_name = forms.CharField()
    url=forms.CharField()