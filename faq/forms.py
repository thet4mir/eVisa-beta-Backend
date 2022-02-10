from django import forms

from .models import Faq


class FaqSortForm(forms.Form):

    orders = forms.ModelMultipleChoiceField(queryset=Faq.objects.all())

    def _get_ordered(self, pk_orders, items):
        items_mapped = {item.pk: item for item in items}

        return [
            items_mapped[pk]
            for pk in pk_orders
        ]

    def clean_orders(self):
        pk_orders = self.data.get('orders')
        faq_list = self.cleaned_data.get('orders')

        return self._get_ordered(pk_orders, faq_list)


default_error_messages = {
    'required': 'оруулна уу!',
    'max_length': "%(limit_value)d-с илүүгүй урттай оруулна уу!",
    'min_length': "%(limit_value)d-с багагүй урттай оруулна уу!",
}


class FaqForm(forms.ModelForm):

    class Meta:
        model = Faq
        fields = ('question', 'answer')

        error_messages = {
            'question': default_error_messages,
            'answer': default_error_messages,
        }
