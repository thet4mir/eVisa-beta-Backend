from django import forms
from .models import Field, FieldText, FieldDate, FieldChoice


default_error_messages = {
    'required': 'оруулна уу!',
    'max_length': "%(limit_value)d-с илүүгүй урттай оруулна уу!",
    'min_length': "%(limit_value)d-с багагүй урттай оруулна уу!",
}


class FieldChoiceForm(forms.ModelForm):

    class Meta:
        model = FieldChoice

        fields = ('label', 'code_name',)

        error_messages = {
            'label': default_error_messages,
            'code_name': default_error_messages,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_permitted = False

    def clean(self, *args, **kwargs):

        clean_data = super().clean()

        label = clean_data.get('label')
        code_name = clean_data.get('code_name')
        if not code_name:
            self.add_error('code_name', 'Оруулна уу!')

        if not label:
            self.add_error('label', 'Оруулна уу!')


class FieldDateForm(forms.ModelForm):
    class Meta:
        model = FieldDate

        fields = (
            'max_kind',
            'max_now_delta',
            'max_date',
            'max_date_error',
            'min_kind',
            'min_now_delta',
            'min_date',
            'min_date_error',
        )

        error_messages = {
            'max_kind': default_error_messages,
            'max_now_delta': default_error_messages,
            'max_date': default_error_messages,
            'max_date_error': default_error_messages,
            'min_kind': default_error_messages,
            'min_now_delta': default_error_messages,
            'min_date': default_error_messages,
            'min_date_error': default_error_messages,
        }


class FieldTextForm(forms.ModelForm):

    class Meta:
        model = FieldText

        fields = (
            'min_length',
            'min_length_error',
            'max_length',
            'max_length_error',
            'regex_chars',
            'regex_chars_error',
        )

        error_messages = {
            'min_length': default_error_messages,
            'min_length_error': default_error_messages,
            'max_length': default_error_messages,
            'max_length_error': default_error_messages,
            'regex_chars': default_error_messages,
            'regex_chars_error': default_error_messages,
        }

    def clean(self, *args, **kwargs):

        cleaned_data = super().clean()
        min_length = cleaned_data.get('min_length')
        max_length = cleaned_data.get('max_length')

        if min_length and max_length:
            if max_length <= min_length:
                self.add_error('max_length', 'Тэмдэгтийн зөвшөөрөх дээд хэмжээ доод хэмжээнээс бага байж болохгүй!')

        if max_length and int(max_length) > 4000:
            self.add_error('max_length', 'Тэмдэгтийн урт хамгийн ихдээ 4000 байна!')

        if min_length and int(min_length) > 4000:
            self.add_error('min_length', 'Тэмдэгтийн урт хамгийн ихдээ 4000 байна!')


class FieldForm(forms.ModelForm):

    is_required = forms.CharField(required=False)
    is_required_error = forms.CharField(required=False)

    class Meta:
        model = Field

        fields = ('label', 'code_name', 'kind', 'description', 'is_required', 'is_required_error',)

        error_messages = {
            'label': default_error_messages,
            'code_name': default_error_messages,
            'kind': default_error_messages,
            'description': default_error_messages,
        }

    def clean(self):
        cleaned_data = super().clean()
        instance = self.instance
        code_name = cleaned_data.get('code_name')
        kind = cleaned_data.get('kind')
        is_required = cleaned_data.get('is_required')

        if instance.pk and instance.is_fixed and instance.code_name != code_name:
            self.add_error('code_name', 'Fixed field-ийг засах боломжгүй!')

        if instance.pk and instance.is_fixed and instance.kind != kind:
            self.add_error('kind', 'Fixed field-ийг засах боломжгүй!')
