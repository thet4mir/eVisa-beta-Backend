from django import forms
from .models import Document, DocumentField
from visa.field.models import Field


default_error_messages = {
    'required': 'оруулна уу!',
    'max_length': "%(limit_value)d-с илүүгүй урттай оруулна уу!",
    'min_length': "%(limit_value)d-с багагүй урттай оруулна уу!",
}


class DocumentFieldForm(forms.ModelForm):

    class Meta:
        model = DocumentField

        fields = ('field', 'sort_order', )

        error_messages = {
            'field': default_error_messages,
            'sort_order': default_error_messages,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['sort_order'].required = False

    def save(self, *args, **kwargs):
        self.instance.sort_order = DocumentField.objects.get_next_sort_order()
        super().save(*args, **kwargs)


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document

        fields = ('name',)

        error_messages = {
            'name': default_error_messages,
        }

    def __init__(self, *args, child_form_data, **kwargs):
        super().__init__(*args, **kwargs)

        self.error_list = []
        self.fixed_forms = []
        self.forms = []
        additional_fields = []
        fields = Field.objects.filter(is_fixed=True, deleted_at__isnull=True)
        if not self.instance.pk:
            self.fixed_forms = [
                DocumentFieldForm(
                    {
                        'field': field,
                        'sort_order': idx
                    }
                )
                for idx, field in enumerate(fields)
            ]
            additional_fields = child_form_data.get('doc_fields')
        else:
            doc = Document.objects.get(pk=self.instance.pk)
            DocumentField.objects.filter(document=doc, field__is_fixed=False).delete()

            fixed = [field.id for field in fields]
            payload_fields = child_form_data.get('doc_fields')

            additional_fields = [el for el in payload_fields if el not in fixed]

        if len(additional_fields):
            self.forms = [
                DocumentFieldForm(
                    {
                        'field': field,
                    }
                )
                for field in additional_fields
            ]

    def save(self, *args, **kwargs):
        document = super().save(*args, **kwargs)

        if len(self.fixed_forms):
            for form in self.fixed_forms:
                form.instance.document = document
                form.save()
        if len(self.forms):
            for form in self.forms:
                form.instance.document = document
                form.save()

        return document
