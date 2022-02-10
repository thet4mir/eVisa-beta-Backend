from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from main.decorators import admin_required, json_decode_request_body
from main.utils import JsonResponse

from .models import Faq
from .forms import FaqSortForm, FaqForm


def _get_faq_display(faq):
    return {
        'id': faq.pk,
        'question': faq.question,
        'answer': faq.answer,
        'sort_order': faq.sort_order,
        'is_active': faq.is_active,
        'created_at': faq.created_at,
        'updated_at': faq.updated_at,
    }


@require_GET
@admin_required
def all(request):
    qs = Faq.objects.all()

    items_display = [
        _get_faq_display(item)
        for item in qs
    ]

    rsp = {
        'is_success': True,
        'items': items_display,
    }

    return JsonResponse(rsp)


@require_POST
@admin_required
@json_decode_request_body
def save(request, pk=None):

    if pk:
        faq = get_object_or_404(Faq, pk=pk)
        form = FaqForm(request.body_json_decoded, instance=faq)
    else:
        form = FaqForm(request.body_json_decoded)

    rsp = {
        'is_success': False,
        'form_errors': {},
    }

    if form.is_valid():
        if not form.instance.pk:
            form.instance.sort_order = Faq.objects.get_next_sort_order()

        faq = form.save()
        rsp['item'] = _get_faq_display(faq)
        rsp['is_success'] = True
    else:
        rsp['form_errors'] = form.errors

    return JsonResponse(rsp)


@require_POST
@admin_required
@json_decode_request_body
def save_sort(request):

    payload = request.body_json_decoded

    form = FaqSortForm(payload)
    if not form.is_valid():
        return HttpResponseBadRequest('{"is_success": false}')

    faq_list = form.cleaned_data.get('orders')

    updated_faq_list = []
    for idx, faq in enumerate(faq_list):
        if faq.sort_order != idx:
            faq.sort_order = idx
            updated_faq_list.append(faq)
    Faq.objects.bulk_update(updated_faq_list, ['sort_order'])

    rsp = {
        'is_success': True,
    }

    return JsonResponse(rsp)


@require_GET
@admin_required
def detail(request, pk):
    faq = get_object_or_404(Faq, pk=pk)
    rsp = {
        'item': _get_faq_display(faq),
        'is_success': True,
    }
    return JsonResponse(rsp)


@require_POST
@admin_required
def delete(request, pk):
    faq = get_object_or_404(Faq, pk=pk)
    faq.delete()
    return JsonResponse({'is_success': True})


@require_POST
@admin_required
@json_decode_request_body
def toggle_active(request, pk):
    payload = request.body_json_decoded

    faq = get_object_or_404(Faq, pk=pk)
    faq.is_active = payload.get('is_active') is True
    faq.save()

    return JsonResponse({'is_success': True})
