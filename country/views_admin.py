from django.utils import timezone
from django.shortcuts import get_object_or_404

from main.decorators import admin_required, json_decode_request_body
from main.utils import JsonResponse

from language.models import Language

from .models import Country, CountryLocale
from .forms import CountryForm, LocaleForm

from log.models import Log


def _get_country_display(country, language):

    locale = CountryLocale.objects.filter(country=country, language=language).first()
    if locale:
        locale_fields = {
            'name': locale.name,
            'nationality': locale.nationality,
        }
    else:
        locale_fields = {}

    return {
        'id': country.id,
        'is_active': country.is_active,
        'code_alpha2': country.code_alpha2,
        'code_alpha3': country.code_alpha3,
        'code_numeric': country.code_numeric,
        'created_at': country.created_at,
        'updated_at': country.updated_at,
        **locale_fields,
    }


@admin_required
def all(request):
    language = Language.objects.get(is_default=True)
    countries = Country.objects.filter(deleted_at__isnull=True)

    all_countries = [
        _get_country_display(country, language)
        for country in countries
    ]

    rsp = {
        'is_success': True,
        'items': all_countries,
    }

    return JsonResponse(rsp)


@admin_required
def detail(request, pk):
    language = Language.objects.get(is_default=True)
    country = get_object_or_404(Country, pk=pk, deleted_at__isnull=True)
    rsp = {
        'is_success': True,
        'item': _get_country_display(country, language),
    }
    return JsonResponse(rsp)


@admin_required
@json_decode_request_body
def save(request, pk=None):

    payload = request.body_json_decoded
    language = Language.objects.get(is_default=True)

    if pk:
        country = get_object_or_404(Country, pk=pk, deleted_at__isnull=True)
        locale = get_object_or_404(CountryLocale, country=country, language=language)

        form = CountryForm(payload, instance=country)
        form_locale = LocaleForm(payload, instance=locale)
        log_kind = Log.KIND_CREATE
    else:
        form = CountryForm(payload)
        form_locale = LocaleForm(payload)
        log_kind = Log.KIND_UPDATE

    rsp = {
        'is_success': False,
        'form_errors': {}
    }

    if form.is_valid() and form_locale.is_valid():
        country = form.save()
        Log.objects.create(
            model_name=country._meta.model.__name__,
            instance_id=country.pk,
            payload=payload,
            kind=log_kind,
            created_by=request.user
        )

        if not form_locale.instance.pk:
            form_locale.instance.language = language
            form_locale.instance.country = country
        locale = form_locale.save()
        Log.objects.create(
            model_name=locale._meta.model.__name__,
            instance_id=locale.pk,
            payload=payload,
            kind=log_kind,
            created_by=request.user
        )

        rsp['is_success'] = True
        rsp['item'] = _get_country_display(country, language)
    else:
        rsp['form_errors'] = {**form_locale.errors, **form.errors}

    return JsonResponse(rsp)


@admin_required
@json_decode_request_body
def toggle_active(request, pk):

    payload = request.body_json_decoded

    country = get_object_or_404(Country, pk=pk, deleted_at__isnull=True)
    Log.objects.create(
        model_name=country._meta.model.__name__,
        instance_id=country.pk,
        payload=payload,
        kind=Log.KIND_UPDATE,
        created_by=request.user
    )

    country.is_active = payload.get('is_active') is True
    country.save()

    rsp = {
        'is_success': True
    }

    return JsonResponse(rsp)


@admin_required
def delete(request, pk):

    country = get_object_or_404(Country, pk=pk)
    country.deleted_at = timezone.now()
    country.save()
    Log.objects.create(
        model_name=country._meta.model.__name__,
        instance_id=country.pk,
        kind=Log.KIND_DELETE,
        created_by=request.user
    )

    locale = CountryLocale.objects.filter(country=country).last()
    Log.objects.create(
        model_name=locale._meta.model.__name__,
        instance_id=locale.pk,
        kind=Log.KIND_DELETE,
        created_by=request.user
    )

    rsp = {
        'is_success': True
    }

    return JsonResponse(rsp)
