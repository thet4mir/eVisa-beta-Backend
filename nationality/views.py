from django.shortcuts import get_object_or_404

from main.decorators import admin_required, json_decode_request_body
from main.utils import JsonResponse

from language.models import Language

from .forms import NationalityForm
from .forms import NationalityLocaleForm
from .models import Nationality
from .models import NationalityLocale


def _get_nationality_display(nationality, language):
    locale = get_object_or_404(NationalityLocale, nationality=nationality, language=language)
    return {
        'id': nationality.id,
        'name': locale.name,
        'country': nationality.country_id,
        'is_active': nationality.is_active,
        'created_at': nationality.created_at,
        'updated_at': nationality.updated_at,
    }


@admin_required
def all(request):

    language = Language.objects.get(is_default=True)
    nationalities = Nationality.objects.all()

    all_nationalities = [
        _get_nationality_display(nationality, language)
        for nationality in nationalities
    ]

    rsp = {
        'is_success': True,
        'items': all_nationalities
    }

    return JsonResponse(rsp)


@admin_required
@json_decode_request_body
def save(request, pk=None):

    payload = request.body_json_decoded
    language = Language.objects.get(is_default=True)

    if pk:
        nationality = get_object_or_404(Nationality, pk=pk)
        locale = get_object_or_404(NationalityLocale, nationality=nationality, language=language)

        form = NationalityForm(payload, instance=nationality)
        form_locale = NationalityLocaleForm(payload, instance=locale)
    else:
        form = NationalityForm(payload)
        form_locale = NationalityLocaleForm(payload)

    rsp = {
        'is_success': False,
        'form_errors': {}
    }

    if form.is_valid() and form_locale.is_valid():
        nationality = form.save()

        if not form_locale.instance.pk:
            form_locale.instance.nationality = nationality
            form_locale.instance.language = language

        form_locale.save()

        rsp['is_success'] = True
        rsp['item'] = _get_nationality_display(nationality, language)
    else:
        rsp['form_errors'] = {
            **form.errors,
            **form_locale.errors,
        }

    return JsonResponse(rsp)


@admin_required
@json_decode_request_body
def toggle_active(request, pk):

    nationality = get_object_or_404(Nationality, pk=pk)
    payload = request.body_json_decoded

    nationality.is_active = payload.get('is_active') is True
    nationality.save()

    rsp = {
        'is_success': True
    }

    return JsonResponse(rsp)


@admin_required
def delete(request, pk):

    nationality = get_object_or_404(Nationality, pk=pk)
    locales = NationalityLocale.objects.filter(nationality=nationality)

    locales.delete()
    nationality.delete()
    rsp = {
        'is_success': True
    }

    return JsonResponse(rsp)
