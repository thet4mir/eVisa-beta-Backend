from django.views.decorators.http import require_POST

from main.utils import JsonResponse
from main.decorators import admin_required
from .models import Log


@require_POST
@admin_required
def list(request):

    logs = Log.objects.all()

    log_list = [
        {
            'model_name': log.model_name,
            'instance_id': log.instance_id,
            'payload': log.payload,
            'kind': log.kind,
            'created_by': log.created_by_id,
            'created_at': log.created_at,
        }
        for log in logs
    ]

    rsp = {
        'is_success': True,
        'items': log_list
    }

    return JsonResponse(rsp)
