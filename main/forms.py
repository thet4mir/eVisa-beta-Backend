from django import forms


error_messages = {

    forms.IntegerField: {
        'required': 'оруулна уу!',
        'invalid': 'Тоо оруулна уу!',
        'max_value': '%(limit_value)s-с ихгүй оруулна уу!',
        'min_value': '%(limit_value)s-с багагүй оруулна уу!',
    },

    forms.CharField: {
        'required': 'оруулна уу!',
        'max_length': "%(limit_value)d-с илүүгүй урттай оруулна уу!",
        'min_length': "%(limit_value)d-с багагүй урттай оруулна уу!",
    },

    forms.BooleanField: {
        'required': 'оруулна уу!',
    },

    forms.NullBooleanField: {
        'required': 'оруулна уу!',
    }

}


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            klass = field.__class__
            if klass in error_messages:
                field.error_messages = error_messages[field.__class__]


class BaseModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            klass = field.__class__
            if klass in error_messages:
                field.error_messages = error_messages[field.__class__]
