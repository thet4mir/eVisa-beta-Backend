from django.views.decorators.http import require_GET

from main.utils import JsonResponse
from .models import Faq


def _get_faq_display(faq):
    return {
        'question': faq.question,
        'answer': faq.answer,
    }


@require_GET
def all(request):

    qs = Faq.objects
    qs = qs.filter(is_active=True)
    qs = qs.values_list('question', 'answer', named=True)

    items_display = [
        _get_faq_display(item)
        for item in qs
    ]

    rsp = {
        'is_success': True,
        'items': items_display,
    }

    return JsonResponse(rsp)
