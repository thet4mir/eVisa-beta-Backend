from main.utils import JsonResponse
from .models import VisaKind, VisaKindDocument, VisaKindDiscount
from visa.document.models import DocumentField
from visa.field.models import Field, FieldDate, FieldText, FieldChoice
from django.views.decorators.http import require_POST


def _get_sub_field_information(field):

    more = {}

    if field.kind == Field.KIND_TEXT:
        field_text = FieldText.objects.get(field=field)
        more = {
            'min_length': field_text.min_length,
            'min_length_error': field_text.min_length_error,
            'max_length': field_text.max_length,
            'max_length_error': field_text.max_length_error,
            'regex_chars': field_text.regex_chars,
            'regex_chars_error': field_text.regex_chars_error,
        }
    elif field.kind == Field.KIND_DATE:
        field_date = FieldDate.objects.get(field=field)
        more = {
            'max_kind': field_date.max_kind,
            'max_now_delta': field_date.max_now_delta.total_seconds() if field_date.max_now_delta else None,
            'max_date': field_date.max_date,
            'max_date_error': field_date.max_date_error,
            'min_kind': field_date.min_kind,
            'min_now_delta': field_date.min_now_delta.total_seconds() if field_date.min_now_delta else None,
            'min_date': field_date.min_date,
            'min_date_error': field_date.min_date_error,
        }
    else:
        field_choice = FieldChoice.objects.filter(field=field)
        choices = []
        for choice in field_choice:
            choices.append({
                'id': choice.id,
                'label': choice.label,
                'code_name': choice.code_name,
            })

        more = {
            'options': choices
        }

    return more


def _get_fixed_fields():
    fields = Field.objects.filter(is_fixed=True)

    doc_fields = []
    for field in fields:
        doc_fields.append({
            'id': field.id,
            'code_name': field.code_name,
            'label': field.label,
            'kind': field.kind,
            'description': field.description,
            'is_required': field.is_required,
            'is_required_error': field.is_required_error,
            **_get_sub_field_information(field),
        })

    KIND_IMAGE = 4

    doc_fields.append({
        'code_name': 'picture',
        'label': 'Photo',
        'kind': KIND_IMAGE,
        'is_fixed': True,
        'description': '',
        'is_required': True,
        'is_required_error': 'This field is required!',
    })
    doc_fields.append({
        'code_name': 'documentPicture',
        'label': 'Document Image',
        'kind': KIND_IMAGE,
        'is_fixed': True,
        'description': '',
        'is_required': True,
        'is_required_error': 'This field is required!',
    })

    return doc_fields


def _get_doc_fields_display(document):

    doc_field_list = [] + _get_fixed_fields()
    doc_fields = DocumentField.objects.filter(document=document, field__is_fixed=False).order_by('sort_order')

    for doc_field in doc_fields:
        doc_field_list.append({
            'id': doc_field.field.id,
            'code_name': doc_field.field.code_name,
            'label': doc_field.field.label,
            'kind': doc_field.field.kind,
            'description': doc_field.field.description,
            'is_required': doc_field.field.is_required,
            'is_required_error': doc_field.field.is_required_error,
            **_get_sub_field_information(doc_field.field),
        })

    return doc_field_list


def _get_visa_kind_document_display(visa_kind):

    documents = VisaKindDocument.objects.filter(visa_kind=visa_kind, document__is_active=True)
    documents_display = []

    for document in documents:
        documents_display.append({
            'id': document.document.id,
            'name': document.document.name,
            'fields': _get_doc_fields_display(document.document),
        })

    return documents_display


def _get_visa_exempt_country(visa_kind):
    countries = visa_kind.visa_exempt_country.all()

    country_list = [
        country.id
        for country in countries
    ]

    return country_list


def _get_fee_exempt_country(visa_kind):

    countries = visa_kind.fee_exempt_country.all()

    country_list = [
        country.id
        for country in countries
    ]

    return country_list


def _get_discount_display(visa_kind):

    discounts = VisaKindDiscount.objects.filter(visa_kind=visa_kind)

    discount_list = [
        {
            'num_person': discount.num_person,
            'percent': discount.percent,
        }
        for discount in discounts
    ]

    return discount_list


@require_POST
def details(request, pk):

    visa_kind = VisaKind.objects.get(pk=pk, is_active=True)
    item = {
        'id': visa_kind.id,
        'title': visa_kind.title,
        'description': visa_kind.description,
        'code_name': visa_kind.code_name,
        'days_stay': visa_kind.days_stay,
        'days_valid': visa_kind.days_valid,
        'entry_kind': visa_kind.entry_kind,
        'fee_person': float(visa_kind.fee_person),
        'documents': _get_visa_kind_document_display(visa_kind),
        'visa_exempt_country': _get_visa_exempt_country(visa_kind),
        'fee_exempt_country': _get_fee_exempt_country(visa_kind),
        'discount_list': _get_discount_display(visa_kind),
    }
    rsp = {
        'is_success': True,
        'item': item,
    }

    return JsonResponse(rsp)


def _get_visa_kind_list_display(visa_kind):

    visa_kind_list = [
        {
            'id': kind.id,
            'title': kind.title,
            'description': kind.description,
            'code_name': kind.code_name,
            'days_stay': kind.days_stay,
            'days_valid': kind.days_valid,
            'entry_kind': kind.entry_kind,
            'fee_person': float(kind.fee_person),
        }
        for kind in visa_kind
    ]

    return visa_kind_list


@require_POST
def list(request):

    visa_kind = VisaKind.objects.filter(is_active=True)
    rsp = {
        'is_success': True,
        'items': _get_visa_kind_list_display(visa_kind)
    }

    return JsonResponse(rsp)
