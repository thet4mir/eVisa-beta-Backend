from django.utils import timezone
from django.shortcuts import get_object_or_404
from main.utils import JsonResponse
from main.decorators import admin_required, json_decode_request_body
from django.views.decorators.http import require_POST

from .models import Document, DocumentField
from .forms import DocumentForm
from visa.field.models import Field, FieldDate, FieldText, FieldChoice


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
            'code_name': field.code_name,
            'label': field.label,
            'kind': field.kind,
            'is_fixed': field.is_fixed,
            'description': field.description,
            'is_required': field.is_required,
            'is_required_error': field.is_required_error,
            'created_at': field.created_at,
            'updated_at': field.updated_at,
            **_get_sub_field_information(field),
        })

    doc_fields.append({
        'code_name': 'nationality',
        'label': 'Улс',
        'kind': Field.KIND_TEXT,
        'is_fixed': True,
        'description': '',
        'is_required': True,
        'is_required_error': 'This field is required!',
    })
    doc_fields.append({
        'code_name': 'picture',
        'label': 'Цээж зураг',
        'kind': Field.KIND_TEXT,
        'is_fixed': True,
        'description': '',
        'is_required': True,
        'is_required_error': 'This field is required!',
    })
    doc_fields.append({
        'code_name': 'documentPicture',
        'label': 'Бичиг баримтын зураг',
        'kind': Field.KIND_TEXT,
        'is_fixed': True,
        'description': '',
        'is_required': True,
        'is_required_error': 'This field is required!',
    })

    return doc_fields


def _get_doc_fields_display(doc):

    doc_field_list = [] + _get_fixed_fields()
    doc_fields = DocumentField.objects.filter(document=doc, field__is_fixed=False)

    for doc_field in doc_fields:

        doc_field_list.append({
            'id': doc_field.field.id,
            'code_name': doc_field.field.code_name,
            'label': doc_field.field.label,
            'kind': doc_field.field.kind,
            'is_fixed': doc_field.field.is_fixed,
            'description': doc_field.field.description,
            'is_required': doc_field.field.is_required,
            'is_required_error': doc_field.field.is_required_error,
            'sort_order': doc_field.sort_order,
            'created_at': doc_field.created_at,
            'updated_at': doc_field.updated_at,
            **_get_sub_field_information(doc_field.field),
        })

    return doc_field_list


def _get_doc_display(doc):
    return {
        'id': doc.id,
        'name': doc.name,
        'is_active': doc.is_active,
        'created_at': doc.created_at,
        'updated_at': doc.updated_at,
        'fields': _get_doc_fields_display(doc)
    }


def _get_doc_list_display(doc):
    return {
        'id': doc.id,
        'name': doc.name,
        'is_active': doc.is_active,
        'created_at': doc.created_at,
        'updated_at': doc.updated_at,
    }


@require_POST
@admin_required
def all(request):

    documents = Document.objects.filter(deleted_at__isnull=True)

    doc_list = [
        _get_doc_list_display(document)
        for document in documents
    ]

    rsp  = {
        'is_success': True,
        'items': doc_list
    }

    return JsonResponse(rsp)


@require_POST
@admin_required
@json_decode_request_body
def save(request, pk=None):

    rsp = {
        'is_success': False
    }
    payload = request.body_json_decoded

    if pk:
        document = get_object_or_404(Document, deleted_at__isnull=True, pk=pk)
        form = DocumentForm(payload, child_form_data=payload, instance=document)
    else:
        form = DocumentForm(payload, child_form_data=payload)

    if form.is_valid():
        doc = form.save()

        rsp['is_success'] = True
        rsp['item'] = _get_doc_display(doc)
    else:
        rsp['form_errors'] = form.errors

    return JsonResponse(rsp)


@require_POST
@admin_required
def details(request, pk):

    doc = get_object_or_404(Document, deleted_at__isnull=True, pk=pk)

    rsp = {
        'is_success': True,
        'item': _get_doc_display(doc)
    }

    return JsonResponse(rsp)


@require_POST
@admin_required
def delete(request, pk):

    rsp = {
        "is_success": False,
    }
    document = get_object_or_404(Document, deleted_at__isnull=True, pk=pk)
    if not document.is_active:
        document.deleted_at = timezone.now()
        document.save()
        rsp['is_success'] = True
    else:
        rsp['error'] = 'Идэвхтэй Бичиг баримтыг устгах боломжгүй!'

    return JsonResponse(rsp)


@require_POST
@admin_required
@json_decode_request_body
def toggle_active(request, pk):

    document = get_object_or_404(Document, deleted_at__isnull=True, pk=pk)
    document.is_active = request.body_json_decoded.get('is_active') is True
    document.save()

    rsp = {
        "is_success": True,
    }

    return JsonResponse(rsp)
