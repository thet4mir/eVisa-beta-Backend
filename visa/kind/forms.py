from django import forms
from .models import VisaKind, VisaKindDiscount


default_error_messages = {
    'required': 'оруулна уу!',
    'max_length': "%(limit_value)d-с илүүгүй урттай оруулна уу!",
    'min_length': "%(limit_value)d-с багагүй урттай оруулна уу!",
}


class KindDiscountForm(forms.ModelForm):

    class Meta:
        model = VisaKindDiscount

        fields = ('num_person', 'percent',)

        error_messages = {
            'num_person': default_error_messages,
            'percent': default_error_messages,
        }

    def clean(self, *args, **kwargs):

        clean_data = super().clean()

        num_person = clean_data.get('num_person')
        percent = clean_data.get('percent')

        if num_person and num_person < 1:
            self.add_error('num_person', '1 буюу түүнээс дээш утга оруулна уу!')

        if percent and not (0 < percent <= 100):
            self.add_error('percent', '0.01-ээс 100-ын хооронд утга оруулна уу!')


class VisaKindForm(forms.ModelForm):

    class Meta:
        model = VisaKind

        fields = (
            'title',
            'description',
            'code_name',
            'is_active',
            'days_stay',
            'days_valid',
            'entry_kind',
            'fee_person',
            'documents',
            'visa_exempt_country',
            'fee_exempt_country',
        )

        error_messages = {
            'title': default_error_messages,
            'description': default_error_messages,
            'code_name': default_error_messages,
            'is_active': default_error_messages,
            'days_stay': default_error_messages,
            'days_valid': default_error_messages,
            'entry_kind': default_error_messages,
            'fee_person': default_error_messages,
            'documents': default_error_messages,
            'visa_exempt_country': default_error_messages,
            'fee_exempt_country': default_error_messages,
        }

    def clean(self, *args, **kwargs):

        clean_data = super().clean()

        days_stay = clean_data.get('days_stay')
        days_valid = clean_data.get('days_valid')

        if days_valid < days_stay:
            self.add_error('days_stay', 'Хүчинтэй хугацаанаас хэтэрсэн байна')
