from django.forms.models import modelformset_factory

from django.utils import timezone
from main.utils import JsonResponse
from django.shortcuts import get_object_or_404
from main.decorators import admin_required, json_decode_request_body
from django.views.decorators.http import require_POST
from .models import Field, FieldChoice, FieldDate, FieldText
from .forms import (
    FieldForm,
    FieldTextForm,
    FieldDateForm,
    FieldChoiceForm,
)


def _get_kind_display(field):
    if field.kind == Field.KIND_TEXT:
        field_text = FieldText.objects.get(field=field)
        return {
            "max_length": field_text.max_length,
            "max_length_error": field_text.max_length_error,
            "min_length": field_text.min_length,
            "min_length_error": field_text.min_length_error,
            'regex_chars': field_text.regex_chars,
            'regex_chars_error': field_text.regex_chars_error
        }

    elif field.kind == Field.KIND_DATE:
        field_date = FieldDate.objects.get(field=field)

        return {
            "max_kind": field_date.max_kind,
            "max_now_delta": field_date.max_now_delta.total_seconds() if field_date.max_now_delta else None,
            "max_date": field_date.max_date,
            "max_date_error": field_date.max_date_error,
            "min_kind": field_date.min_kind,
            "min_now_delta": field_date.min_now_delta.total_seconds() if field_date.min_now_delta else None,
            "min_date": field_date.min_date,
            "min_date_error": field_date.min_date_error,
        }
    else:
        field_choices = FieldChoice.objects.filter(field=field, is_deleted=False)
        all_choices = []
        for choice in field_choices:
            all_choices.append({
                'label': choice.label,
                'code_name': choice.code_name,
            })

        return {'options': all_choices}


def _get_field_display(field):

    details = {
        "id": field.id,
        "label": field.label,
        "code_name": field.code_name,
        "description": field.description,
        "is_required": field.is_required,
        "is_required_error": field.is_required_error,
        "kind": field.kind,
        "is_fixed": field.is_fixed,
        "created_at": field.created_at,
        "updated_at": field.updated_at,
    }
    details.update(_get_kind_display(field))

    return details


@require_POST
@admin_required
@json_decode_request_body
def all(request):

    fields = Field.objects.filter(deleted_at=None)
    field_list = [
        _get_field_display(field)
        for field in fields
    ]

    rsp = {
        "is_success": True,
        "items": field_list
    }
    return JsonResponse(rsp)


def build_formset_form_data(form_number, **data):

    form = {}

    for key, value in data.items():
        form_key = f"form-{form_number}-{key}"
        form[form_key] = value

    return form


def choose_sub_form(payload, field=None):
    if payload.get('kind') == Field.KIND_TEXT:
        if field:
            sub_field = FieldText.objects.get(field=field)
            form = FieldTextForm(payload, instance=sub_field)
        else:
            form = FieldTextForm(payload)

    elif payload.get('kind') == Field.KIND_DATE:
        if field:
            sub_field = FieldDate.objects.get(field=field)
            form = FieldDateForm(payload, instance=sub_field)
        else:
            form = FieldDateForm(payload)
    else:
        if payload.get('options'):
            choice_field = {
                'form-TOTAL_FORMS': f"{len(payload.get('options'))}",
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }

            for idx, form_data in enumerate(payload.get('options')):
                form_dict = build_formset_form_data(idx, **form_data)
                choice_field.update(form_dict)

            FieldChoiceFormset = modelformset_factory(FieldChoice, form=FieldChoiceForm)
            queryset = FieldChoice.objects.none()
            form = FieldChoiceFormset(choice_field, queryset=queryset)
        else:
            return False
    return form


@require_POST
@admin_required
@json_decode_request_body
def save(request, pk=None):

    payload = request.body_json_decoded
    choice_form_error = False

    if pk:
        field = get_object_or_404(Field, pk=pk)
        form = FieldForm(payload, instance=field)
        if choose_sub_form(payload, field):
            sub_form = choose_sub_form(payload, field)
            sub_form_valid = sub_form.is_valid()
        else:
            sub_form_valid = False
            choice_form_error = {'options': 'Та сонголтуудыг оруулна уу!'}
    else:
        form = FieldForm(payload)
        if choose_sub_form(payload):
            sub_form = choose_sub_form(payload)
            sub_form_valid = sub_form.is_valid()
        else:
            sub_form_valid = False
            choice_form_error = {'options': 'Та сонголтуудыг оруулна уу!'}

    rsp = {
        'is_success': False,
        'form_errors': []
    }

    form_valid = form.is_valid()
    if form_valid and sub_form_valid:

        field = form.save()
        if payload.get('kind') == Field.KIND_CHOICES:

            FieldChoice.objects.filter(field=field).update(is_deleted=True)
            for field_form in sub_form:
                field_form.instance.field = field

            sub_form.save()
        else:
            sub_form.instance.field = field
            sub_form.save()

        rsp['is_success'] = True
        rsp['item'] = _get_field_display(field)
    else:
        rsp['form_errors'] = form.errors

        if not sub_form_valid:
            if payload.get('kind') == Field.KIND_CHOICES:
                if choice_form_error:
                    rsp['form_errors'].update(choice_form_error)
                else:
                    rsp['form_errors'].update({'options': sub_form.errors})
            else:
                rsp['form_errors'].update(**sub_form.errors)

    return JsonResponse(rsp)


@require_POST
@admin_required
@json_decode_request_body
def delete(request, pk):

    rsp = {
        "is_success": False,
    }
    field = get_object_or_404(Field, pk=pk)
    if not field.is_fixed:
        field.deleted_at = timezone.now()
        field.save()
        rsp['is_success'] = True
    else:
        rsp['is_success'] = False
        rsp['errors'] = 'Fixed field-ийг устгах боломжгүй!'

    return JsonResponse(rsp)


@require_POST
@admin_required
@json_decode_request_body
def details(request, pk):

    field = get_object_or_404(Field, pk=pk)

    rsp = {
        'is_success': True,
        'item': _get_field_display(field)
    }

    return JsonResponse(rsp)
