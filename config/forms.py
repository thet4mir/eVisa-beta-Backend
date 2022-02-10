from django import forms

from .models import Config


default_error_messages = {
    'required': 'оруулна уу!',
    'max_length':   "%(limit_value)d-с илүүгүй урттай оруулна уу!",
    'min_length':   "%(limit_value)d-с багагүй урттай оруулна уу!",
    'unique':       'Ийм нэртэй тохиргоо үүссэн байна!',
}


class ConfigForm(forms.ModelForm):

    class Meta:
        model = Config
        fields = ['name', 'value']

    def __init__(self, *args, **kwargs):

        payload = args[0]
        instance = self._meta.model.objects.filter(name=payload.get('name')).first()
        if instance:
            kwargs['instance'] = instance

        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].error_messages  = default_error_messages
