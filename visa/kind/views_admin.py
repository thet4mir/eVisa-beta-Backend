from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from country.models import CountryLocale
from main.decorators import admin_required, json_decode_request_body
from main.utils import JsonResponse
from main.utils import get_default_language_code_name

from .forms import VisaKindForm, KindDiscountForm
from .models import VisaKind, VisaKindDiscount


def _get_discounts_display(visa_kind):
    discount_list = []
    discounts = VisaKindDiscount.objects.filter(visa_kind=visa_kind)
    for discount in discounts:
        discount_list.append({
            'id': discount.id,
            'num_person': discount.num_person,
            'percent': discount.percent,
        })

    return discount_list


def _get_country_display(country):

    language_code_name = get_default_language_code_name()

    locale = get_object_or_404(
        CountryLocale,
        country=country,
        language__code_name=language_code_name,
    )

    return {
        'id': country.id,
        'name': locale.name,
    }


def _get_fee_exempt_country_display(visa_kind):

    return [
        _get_country_display(country)
        for country in visa_kind.fee_exempt_country.all()
    ]


def _get_visa_exempt_country_display(visa_kind):

    return [
        _get_country_display(country)
        for country in visa_kind.visa_exempt_country.all()
    ]


def _get_documents_dispay(visa_kind):

    doc_list = []
    for document in visa_kind.documents.all():
        doc_list.append({
            'id': document.id,
            'name': document.name,
        })

    return doc_list


def _get_visa_kind_display(visa_kind):
    return {
        'id': visa_kind.id,
        'title': visa_kind.title,
        'description': visa_kind.description,
        'code_name': visa_kind.code_name,
        'is_active': visa_kind.is_active,
        'days_stay': visa_kind.days_stay,
        'days_valid': visa_kind.days_valid,
        'entry_kind': visa_kind.entry_kind,
        'fee_person': visa_kind.fee_person,
        'documents': _get_documents_dispay(visa_kind),
        'visa_exempt_countries': _get_visa_exempt_country_display(visa_kind),
        'fee_exempt_countries': _get_fee_exempt_country_display(visa_kind),
        'discount_list': _get_discounts_display(visa_kind),
        'created_at': visa_kind.created_at,
        'updated_at': visa_kind.updated_at,
    }


@require_POST
@admin_required
@json_decode_request_body
def list(request):
    visa_kinds = VisaKind.objects.filter(deleted_at=None)

    kind_list = [
        _get_visa_kind_display(kind)
        for kind in visa_kinds
    ]

    rsp = {
        'is_success': True,
        'items': kind_list
    }

    return JsonResponse(rsp)


def build_formset_form_data(form_number, **data):

    form = {}

    for key, value in data.items():
        form_key = f"form-{form_number}-{key}"
        form[form_key] = value

    return form


@require_POST
@admin_required
@json_decode_request_body
def save(request, pk=None):

    payload = request.body_json_decoded
    discount_list = len(payload.get('discount_list')) if payload.get('discount_list') else 0
    discount_payload = {
        'form-TOTAL_FORMS': f"{discount_list}",
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',

    }
    if discount_list != 0:
        for idx, form_data in enumerate(payload.get('discount_list')):
            form_dict = build_formset_form_data(idx, **form_data)
            discount_payload.update(form_dict)

    if pk:
        visa_kind = get_object_or_404(VisaKind, pk=pk)
        form = VisaKindForm(payload, instance=visa_kind)
    else:
        form = VisaKindForm(payload)

    rsp = {
        'is_success': False
    }

    DiscountFormset = modelformset_factory(VisaKindDiscount, form=KindDiscountForm)
    queryset = VisaKindDiscount.objects.none()
    formset = DiscountFormset(discount_payload, queryset=queryset)

    form_valid = form.is_valid()
    formset_valid = formset.is_valid()
    if form_valid and formset_valid:
        visa_kind = form.save(commit=False)
        visa_kind.save()
        form.save_m2m()

        VisaKindDiscount.objects.filter(visa_kind=visa_kind).delete()
        for discount_form in formset:
            discount_form.instance.visa_kind = visa_kind
        formset.save()

        rsp['is_success'] = True
        rsp['item'] = _get_visa_kind_display(visa_kind)
    else:
        rsp['form_errors'] = form.errors

        if not formset_valid:
            rsp['form_errors'].update({'discount_list': formset.errors})

    return JsonResponse(rsp)


@require_POST
@admin_required
@json_decode_request_body
def delete(request, pk):

    visa_kind = get_object_or_404(VisaKind, pk=pk)

    rsp = {
        'is_success': False
    }

    if not visa_kind.is_active:
        visa_kind.deleted_at = timezone.now()
        visa_kind.save()
        rsp['is_success'] = True
    else:
        rsp['errors'] = "Идэвхтэй төрлийг устгах боломгүй!"

    return JsonResponse(rsp)


@require_POST
@admin_required
@json_decode_request_body
def toggle_active(request, pk):

    payload = request.body_json_decoded
    visa_kind = get_object_or_404(VisaKind, pk=pk)
    visa_kind.is_active = payload.get('is_active') is True
    visa_kind.save()

    rsp = {
        'is_success': True
    }

    return JsonResponse(rsp)


@require_POST
@admin_required
@json_decode_request_body
def details(request, pk):

    visa_kind = get_object_or_404(VisaKind, pk=pk)

    rsp = {
        'is_success': True,
        'item': _get_visa_kind_display(visa_kind)
    }

    return JsonResponse(rsp)
