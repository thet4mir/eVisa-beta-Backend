from django.views.decorators.http import require_GET

from main.utils import JsonResponse
from .models import Language


def _get_language_pub_display(lang):
    return {
        "id": lang.id,
        "name_local": lang.name_local,
        "code_name": lang.code_name,
        "is_default": lang.is_default,
    }


@require_GET
def public_all(request):

    langs = Language.objects.filter(is_active=True)

    languages = [
        _get_language_pub_display(language)
        for language in langs
    ]
    rsp = {
        "is_success": True,
        "items": languages
    }

    return JsonResponse(rsp)
