from django.views.decorators.http import require_POST

from main.decorators import json_decode_request_body
from main.utils import JsonResponse
from main.utils import prefetch_locale

from .models import Country, CountryLocale


def _get_country_display(country):
    locale = country.locales.all().first()
    return {
        'id': country.id,
        'name': locale.name,
    }


def _get_qs_country(lang_code):

    qs = Country.objects
    qs = qs.filter(deleted_at__isnull=True)
    qs = qs.filter(is_active=True)

    qs = qs.prefetch_related(
        prefetch_locale(CountryLocale, lang_code),
    )

    return qs


@require_POST
@json_decode_request_body
def all(request):

    lang_code = request.body_json_decoded.get('language')
    countries = _get_qs_country(lang_code)

    countries_display = [
        _get_country_display(country)
        for country in countries
    ]

    rsp = {
        'is_success': True,
        'items': countries_display,
    }

    return JsonResponse(rsp)
