from django import forms

class EmailForm(forms.Form):
    to_email = forms.EmailField(required=True)