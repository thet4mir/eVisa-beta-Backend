from django.utils import timezone
from main.decorators import admin_required
from main.decorators import json_decode_request_body
from main.utils import send_mail, send_pdf
from main.utils import JSONEncoder
from main.utils import JsonResponse

from .models import Config
from .forms import ConfigForm
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter


def generate_pdf():

    y = 700
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont('Helvetica', 11)
    p.drawString(220, y, "PDF generated at " + timezone.now().strftime('%Y-%b-%d'))
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()

    return pdf


@admin_required
@json_decode_request_body
def test_send_file(request):

    pdf = generate_pdf()
    send_to = request.body_json_decoded.get('send_to')
    subject = request.body_json_decoded.get('subject')
    body = request.body_json_decoded.get('body')

    mail_result = send_pdf(send_to, subject, '', body, pdf)

    rsp = {
        'is_success': bool(mail_result),
    }

    return JsonResponse(rsp, encoder=JSONEncoder)


@admin_required
@json_decode_request_body
def test_send_mail(request):

    send_to = request.body_json_decoded.get('send_to')
    subject = request.body_json_decoded.get('subject')
    body = request.body_json_decoded.get('body')

    mail_result = send_mail(send_to, subject, '', body)

    rsp = {
        'is_success': bool(mail_result),
    }

    return JsonResponse(rsp)


def _get_config_display(config):
    return {
        'name': config.name,
        'value': config.value,
        'created_at': config.created_at,
        'updated_at': config.updated_at,
    }


@admin_required
def all(request):

    configs = Config.objects.all()
    configs_display = [
        _get_config_display(config)
        for config in configs
    ]

    rsp = {
        'is_success': True,
        'configs': configs_display,
    }
    return JsonResponse(rsp)


@admin_required
@json_decode_request_body
def save(request):

    rsp = {
        'is_success': False,
        'errors': {},
    }

    form = ConfigForm(request.body_json_decoded)

    if form.is_valid():
        form.save()
        rsp['is_success'] = True
    else:
        rsp['errors'] = form.errors

    return JsonResponse(rsp)
