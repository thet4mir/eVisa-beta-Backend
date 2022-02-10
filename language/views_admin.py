from django.shortcuts import get_object_or_404

from main.decorators import admin_required, json_decode_request_body
from main.utils import JsonResponse

from .models import Language
from .forms import LanguageForm


def _get_language_display(lang):
    return {
        "id": lang.id,
        "name": lang.name,
        "name_local": lang.name_local,
        "code_name": lang.code_name,
        "is_active": lang.is_active,
        "is_default": lang.is_default,
        "created_at": lang.created_at,
        "updated_at": lang.updated_at,
    }


@admin_required
def all(request):
    lagnuages = Language.objects.all()

    lang = [
        _get_language_display(language)
        for language in lagnuages
    ]
    rsp = {
        "is_success": True,
        "items": lang
    }
    return JsonResponse(rsp)


@admin_required
@json_decode_request_body
def create(request):
    rsp = {
        'is_success': False,
        'form_errors': {}
    }
    payload = request.body_json_decoded
    form = LanguageForm(payload)

    if form.is_valid():
        lang = form.save()
        rsp['is_success'] = True
        rsp['item'] = _get_language_display(lang)
    else:
        rsp['form_errors'] = form.errors

    return JsonResponse(rsp)


@admin_required
@json_decode_request_body
def toggle_active(request, pk):

    rsp = {
        'is_success': False
    }

    lang = get_object_or_404(Language, pk=pk)
    payload = request.body_json_decoded

    if lang.is_default and lang.is_active:
        rsp['error'] = 'Үндсэн хэлийг идэвхигүй болгох боломжгүй байна!'

    else:
        lang.is_active = payload['is_active'] is True
        lang.save()
        rsp['is_success'] = True

    return JsonResponse(rsp)


@admin_required
def detail(request, pk):

    lang = get_object_or_404(Language, pk=pk)
    rsp = {
        'is_success': True,
        'item': _get_language_display(lang)
    }

    return JsonResponse(rsp)


@admin_required
def set_default(request, pk):

    lang = get_object_or_404(Language, pk=pk)
    rsp = {
        'is_success': False
    }

    if not lang.is_default and lang.is_active:
        lang.is_default = True
        lang.save()
        Language.objects.exclude(pk=lang.pk).update(is_default=False)
        rsp['is_success'] = True
    else:
        rsp['errors'] = 'Идэвхигүй хэлийг default хэл болгох боломжгүй!'
        return JsonResponse(rsp)

    return JsonResponse(rsp)


@admin_required
@json_decode_request_body
def update(request, pk):
    rsp = {
        'is_success': False,
        'form_errors': {}
    }
    lang = get_object_or_404(Language, pk=pk)
    payload = request.body_json_decoded
    form = LanguageForm(payload, instance=lang)

    if form.is_valid():
        form.save()
        rsp['is_success'] = True
        rsp['item'] = _get_language_display(lang)
    else:
        rsp['form_errors'] = form.errors

    return JsonResponse(rsp)


@admin_required
def delete(request, pk):
    rsp = {
        'is_success': False
    }
    lang = get_object_or_404(Language, pk=pk)

    if not lang.is_default:
        lang.delete()
        rsp['is_success'] = True
    else:
        rsp['is_success'] = False
        rsp['error'] = 'Үндсэн хэлийг устгах боломжгүй байна!'

    return JsonResponse(rsp)
