from django import forms

from .models import NationalityLocale, Nationality


default_error_messages = {
    'required': 'оруулна уу!',
    'max_length': "%(limit_value)d-с илүүгүй урттай оруулна уу!",
    'min_length': "%(limit_value)d-с багагүй урттай оруулна уу!",
}


class NationalityForm(forms.ModelForm):

    class Meta:
        model = Nationality

        fields = ('country', 'is_active',)

        error_messages = {
            'country': {
                'required': 'оруулна уу!',
            },
            'is_active': {
                'required': 'оруулна уу!',
            }
        }

    def __init__(self, *args, **kwargs):
        super(NationalityForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].required = True


class NationalityLocaleForm(forms.ModelForm):
    class Meta:
        model = NationalityLocale

        fields = ('name',)

        error_messages = {
            'name': default_error_messages,
        }
