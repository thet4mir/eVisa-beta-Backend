from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from main.decorators import admin_required, json_decode_request_body
from main.utils import JsonResponse
from .models import Error500


def _get_error_display_list(error):
    return {
        "id": error.id,
        "request_scheme": error.request_scheme,
        "request_url": error.request_url,
        "request_method": error.request_method,
        "created_at": error.created_at,
    }


def _get_error_display_detail(error):
    base_display = _get_error_display_list(error)
    return {
        **base_display,
        "request_headers": error.request_headers,
        "request_data": error.request_data,
        "request_body": error.request_body,
        "description": error.description,
    }


@require_POST
@json_decode_request_body
@admin_required
def all(request):

    payload = request.body_json_decoded

    errors = Error500.objects.all().order_by('-created_at')

    all_error = [
        _get_error_display_list(error)
        for error in errors
    ]
    paginator = Paginator(all_error, payload.get('per_page', 25))
    page = payload.get('page', 1)
    result = paginator.get_page(page)

    rsp = {
        "is_success": True,
        "result": result.object_list,
        "total_record": paginator.count,
        "total_page": paginator.num_pages,
        "page": result.number,
    }

    return JsonResponse(rsp)


@require_POST
@admin_required
def details(request, pk):
    error = get_object_or_404(Error500, pk=pk)

    rsp = {
        "is_success": True,
        "item": _get_error_display_detail(error)
    }

    return JsonResponse(rsp)
