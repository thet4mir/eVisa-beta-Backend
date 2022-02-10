import json
import re
from django import forms
from main.utils import create_simple_uploaded_obj, pill_resize_img

from .models import Visa, Person, ValueText, ValueDate, ValueChoice
from visa.kind.models import VisaKindDocument
from visa.document.models import DocumentField, Document
from visa.field.models import FieldDate, FieldText, Field
from django.conf import settings
from visa.person_number.models import VisaPersonNumber
from django.utils import timezone
from django.core.exceptions import ValidationError
from visa.kind.models import VisaKind
from country.models import Country


class VisaFilterForm(forms.Form):
    STATUS_CHOICES = (
        ("", "Бүгд"),
        (Person.STATUS_NEW, "Шинэ Хүсэлт"),
        (Person.STATUS_APPROVE, "Зөвшөөрсөн"),
        (Person.STATUS_DECLINE, "Татгалзсан"),
    )
    text        = forms.CharField(
        min_length=2,
        required=False,
        error_messages={'min_length': ('Хайх утга богино байна!')}
    )
    kind        = forms.ModelChoiceField(queryset=VisaKind.objects.filter(deleted_at=None), required=False)
    country     = forms.ModelChoiceField(queryset=Country.objects.filter(deleted_at=None), required=False)
    start_date  = forms.DateField(required=False)
    end_date    = forms.DateField(required=False)
    status      = forms.ChoiceField(choices=STATUS_CHOICES, required=False)

    def clean(self, *args, **kwargs):

        clean_data = super().clean()
        start_date = clean_data.get('start_date')
        end_date = clean_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            self.add_error('start_date', 'Эхлэх огноо дуусах огнооноос их байж болохгүй!')


class ValueTextForm(forms.ModelForm):

    value = forms.CharField(required=False)

    class Meta:
        model = ValueText

        fields = ('value', 'document_field',)

    def clean(self, *args, **kwargs):

        cleaned_data    = super().clean()
        value           = cleaned_data.get('value', None)
        doc_field  = cleaned_data.get('document_field', None)

        field_text          = FieldText.objects.get(field=doc_field.field)

        min_length          = field_text.min_length
        min_length_error    = field_text.min_length_error
        max_length          = field_text.max_length
        max_length_error    = field_text.max_length_error
        regex_chars         = field_text.regex_chars
        regex_chars_error   = field_text.regex_chars_error

        if doc_field.field.is_required and not value:
            self.add_error('value', doc_field.field.is_required_error)

        elif min_length and len(value) < int(min_length):
            error_message = min_length_error.replace('[limit]', min_length)
            self.add_error('value', error_message)

        elif max_length and len(value) > int(max_length):
            error_message = max_length_error.replace('[limit]', max_length)
            self.add_error('value', error_message)

        elif regex_chars and value:
            try:
                if not bool(re.search(regex_chars, value)):
                    self.add_error('value', regex_chars_error)
            except Exception:
                self.add_error('value', 'character check error')


class ValueDateForm(forms.ModelForm):

    class Meta:
        model = ValueDate

        fields = ('value', 'document_field',)

    def _get_min_limit(self, field_date):

        min_limit = None

        min_kind = field_date.min_kind
        min_delta = field_date.min_now_delta
        min_date = field_date.min_date

        if min_kind == FieldDate.KIND_NOW:
            min_limit = timezone.now()
            if min_delta:
                min_limit += min_delta

        if min_kind == FieldDate.KIND_DATE:
            min_limit = min_date

        return min_limit

    def _get_max_limit(self, field_date):

        max_limit = None

        max_kind = field_date.max_kind
        max_delta = field_date.max_now_delta
        max_date = field_date.max_date

        if max_kind == FieldDate.KIND_NOW:
            max_limit = timezone.now()
            if max_delta:
                max_limit += max_delta

        if max_kind == FieldDate.KIND_DATE:
            max_limit = max_date

        return max_limit

    def clean(self, *args, **kwargs):

        cleaned_data = super().clean()
        value = cleaned_data.get("value", "")
        document_field = cleaned_data.get("document_field", "")

        if document_field:
            field_date = FieldDate.objects.get(field=document_field.field)

            min_limit = self._get_min_limit(field_date)
            max_limit = self._get_max_limit(field_date)

            if document_field.field.is_required and not value:
                self.add_error('value', document_field.field.is_required_error)

            if min_limit and value < min_limit:
                min_error = field_date.min_date_error
                error_message = min_error.replace('[limit]', min_limit.strftime('%Y-%m-%d'))
                self.add_error('value', error_message)

            if max_limit and value > max_limit:
                max_error = field_date.max_date_error
                error_message = max_error.replace('[limit]', max_limit.strftime('%Y-%m-%d'))
                self.add_error('value', error_message)


class ValueChoiceForm(forms.ModelForm):

    class Meta:
        model = ValueChoice

        fields = ('value', 'document_field',)

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        value = cleaned_data.get('value', None)
        document_field = cleaned_data.get('document_field', None)

        if document_field.field.is_required and not value:
            self.add_error('value', document_field.field.is_required_error)


class FieldForm(forms.ModelForm):

    class Meta:
        model = DocumentField

        fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.error_list = []
        values = args[0]['value']
        self.document = args[0]['document']
        self.doc_field = DocumentField.objects.get(pk=values.get('doc_field'))
        payload = {
            'value': values.get('value'),
            'document_field': self.doc_field,
        }

        if self.doc_field.field.kind == Field.KIND_TEXT:
            self.form = ValueTextForm(payload)

        elif self.doc_field.field.kind == Field.KIND_DATE:
            self.form = ValueDateForm(payload)

        elif self.doc_field.field.kind == Field.KIND_CHOICES:
            self.form = ValueChoiceForm(payload)

    def clean(self):
        super().clean()
        if self.doc_field.document != self.document:
            raise ValidationError("This field doesn't included the document that you chose!")

    def is_valid(self):
        return (
            super().is_valid()
            and self.form.is_valid()
        )

    def save(self, *args, **kwargs):

        self.form.instance.person = self.instance.person
        self.form.save()

    @property
    def errors(self):

        if self._errors is None:
            self.full_clean()

            error_list = json.loads(self._errors.as_json())
            for idx, value in error_list.items():
                self.error_list.append({
                    self.doc_field.field.code_name: value[0]['message']
                })

            if self.form.errors:
                error = json.loads(self.form.errors.as_json())
                self.error_list.append({self.doc_field.field.code_name: error['value'][0]['message']})

        return self.error_list


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person

        fields = ('document', 'image_portrait', 'image_document',)

    def __init__(self, payload, files, *args, **kwargs):

        img_document = files.get('image_document')
        img_portrait = files.get('image_portrait')

        if img_document:
            files.update({
                'image_document': create_simple_uploaded_obj(img_document)
            })

        if img_portrait:
            files.update({
                'image_portrait': create_simple_uploaded_obj(img_portrait)
            })

        super().__init__(payload, files, *args, **kwargs)
        self.document = Document.objects.get(pk=payload.get('document'))
        self.visakind_document = VisaKindDocument.objects.filter(
            visa_kind=payload.get('visa_kind'),
            document=payload.get('document')).count()
        self.error_list = []

        self.forms = [
            FieldForm(
                {
                    'document': self.document,
                    'value': value
                }
            )
            for value in payload.get('values')
        ]

    def is_valid(self):
        valid = True
        for form in self.forms:
            if not form.is_valid():
                valid = False

        return (super().is_valid() and valid)

    def clean(self):
        cleaned_data = super().clean()

        image_portrait = cleaned_data.get('image_portrait', None)
        image_document = cleaned_data.get('image_document', None)
        document = cleaned_data.get('document')

        if not image_document:
            self.add_error('image_document', "this field is required!")

        elif image_document.size > settings.DOCUMENT_MAX_UPLOAD_SIZE:
            error = f"Please keep filesize under {int(settings.DOCUMENT_MAX_UPLOAD_SIZE/1000)}kb"
            self.add_error('image_document', error)
        if not image_portrait:
            self.add_error('image_portrait', "this field is required!")
        elif image_portrait.size > settings.PORTRAIT_MAX_UPLOAD_SIZE:
            error = f"Please keep filesize under {int(settings.PORTRAIT_MAX_UPLOAD_SIZE/1000)}kb"
            self.add_error('image_document', error)

        if not document:
            self.add_error('document', "This field is required!")

        if self.visakind_document == 0:
            self.add_error('document', "No longer to approve this kind of document this Visa Type!")

    def save(self, *args, **kwargs):

        person_number = VisaPersonNumber.objects.filter(is_used=False).first()

        if not self.instance.pk and not self.instance.number:
            self.instance.number = person_number.id
            person_number.is_used = True
            person_number.save()

        self.instance.image_portrait.name = f'{person_number.id}.jpeg'
        self.instance.image_document.name = f'{person_number.id}.jpeg'

        self.instance.image_portrait = pill_resize_img(self.instance.image_portrait, 413, 531)
        self.instance.image_document = pill_resize_img(self.instance.image_document, 1476, 1039)

        person = super().save(*args, **kwargs)

        for form in self.forms:
            form.instance.person = person
            form.save()

        return person

    @property
    def errors(self):

        if self._errors is None:
            self.full_clean()
            error_list = json.loads(self._errors.as_json())
            for idx, value in error_list.items():
                self.error_list.append({
                    idx: value[0]['message']
                })

            for form in self.forms:
                if form.errors:
                    self.error_list.append(form.errors)

        return self.error_list


class VisaForm(forms.ModelForm):

    email = forms.CharField()
    phone = forms.CharField()
    address = forms.CharField()

    class Meta:
        model = Visa

        fields = (
            'visa_kind',
            'country',
            'date_of_arrival',
        )

    def __init__(self, *args, child_form_data, **kwargs):
        super().__init__(*args, **kwargs)

        self.error_list = []
        self.num_person = len(child_form_data.get('person'))

        self.forms = [
            PersonForm(
                {
                    'visa_kind': child_form_data.get('visa_kind'),
                    'document': values['document'],
                    'values': values['values'],
                },
                {
                    'image_document': values['image_document'],
                    'image_portrait': values['image_portrait'],
                }
            )
            for values in child_form_data.get('person')
        ]

    def is_valid(self):
        valid = True
        for form in self.forms:
            if not form.is_valid():
                valid = False

        return (super().is_valid() and valid)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        address = cleaned_data.get('address')
        visa_kind = cleaned_data.get('visa_kind', None)

        if not visa_kind.is_active:
            self.add_error('visa_kind', 'The Visa Kind that you choices is deactive ')

        if not email:
            self.add_error('email', "This field is required!")

        if not phone:
            self.add_error('phone', "This field is required!")

        if not address:
            self.add_error('address', "This field is required!")

        if self.num_person == 0:
            raise ValidationError('You must apply with atleast one person information!')

        if self.num_person > 25:
            raise ValidationError('You only can apply with 25 people!')

    def save(self, *args, **kwargs):

        visa = super().save(*args, **kwargs)
        for form in self.forms:
            form.instance.visa = visa
            form.save()

        return visa

    @property
    def errors(self):

        if self._errors is None:
            self.full_clean()
            error_list = json.loads(self._errors.as_json())
            for idx, value in error_list.items():
                key = idx if idx != '__all__' else 'person'
                self.error_list.append({
                    key: value[0]['message']
                })

            error_sum = 0
            child_form_errors = []
            for form in self.forms:
                child_form_errors.append(form.errors)
                error_sum = error_sum + len(form.errors)

            if error_sum:
                self.error_list.append({'person': child_form_errors})

        return self.error_list
