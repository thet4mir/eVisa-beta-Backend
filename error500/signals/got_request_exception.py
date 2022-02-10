import traceback
import json

from django.dispatch import receiver
from django.core.signals import got_request_exception
from django.utils.timezone import localtime, now

from error500.models import Error500


@receiver(got_request_exception)
def save_error500(sender, request, **kwargs):

    try:

        request_scheme = request.scheme
        request_url = request.path
        request_method = request.method
        request_data = json.dumps(request.POST, indent=4, ensure_ascii=False)
        request_body = request.body.decode()
        request_headers = json.dumps(dict(request.headers), indent=4, ensure_ascii=False)
        description = traceback.format_exc()
        Error500.objects.create(
            request_scheme=request_scheme,
            request_url=request_url,
            request_method=request_method,
            request_headers=request_headers,
            request_data=request_data,
            request_body=request_body,
            description=description
        )

    except Exception:

        dt = localtime(now())
        msg_format = '[{datetime}] Could not save Error500 to database.'
        msg = msg_format.format(
            datetime=dt.strftime('%Y-%m-%d'),
        )
        print(msg)
