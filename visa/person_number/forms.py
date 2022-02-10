from django import forms
from main.forms import BaseForm


class GenerateForm(BaseForm):

    length = forms.IntegerField(
        min_value=8,
        max_value=12,
        required=True,
    )

    amount = forms.IntegerField(
        min_value=1,
        max_value=1000000,
        required=True,
    )
