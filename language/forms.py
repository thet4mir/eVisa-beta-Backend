from django import forms
from .models import Language


default_error_messages = {
    'required': 'оруулна уу!',
    'max_length': "%(limit_value)d-с илүүгүй урттай оруулна уу!",
    'min_length': "%(limit_value)d-с багагүй урттай оруулна уу!",
}


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language

        fields = ("name", "name_local", "code_name", "is_active")

        error_messages = {
            'name': default_error_messages,
            'name_local': default_error_messages,
            'code_name': default_error_messages,
            'is_active': {
                'required': 'оруулна уу!',
            }
        }
