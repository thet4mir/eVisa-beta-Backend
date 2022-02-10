import os
import qrcode
from io import BytesIO
from datetime import timedelta
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.conf import settings

from visa.field.models import Field
from visa.document.models import DocumentField
from visa.visa.models import ValueDate, ValueText, ValueChoice


def _get_value_fer_fields(person, doc_field):

    if doc_field.field.kind == Field.KIND_TEXT:
        value_text = ValueText.objects.filter(person=person, document_field=doc_field)
        if value_text.count() != 0:
            return {'value': str(value_text.last().value)}
        else:
            return {'value': ''}
    elif doc_field.field.kind == Field.KIND_DATE:
        value_date = ValueDate.objects.filter(person=person, document_field=doc_field)
        if value_date.count() != 0:
            return {'value': value_date.last().value.strftime("%Y-%m-%d")}
        else:
            return {'value': ''}
    else:
        value_choice = ValueChoice.objects.filter(person=person, document_field=doc_field)
        if value_choice.count() != 0:
            return {'value': str(value_choice.last().value.label)}
        else:
            return {'value': ''}


def _generate_qr_code(person_number):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(person_number)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    img.save(f'{settings.STATIC_ROOT}/qr.png')


def GeneratePDF(person):

    now = timezone.now().date()
    expiry = now + timedelta(days=person.visa.days_valid)
    doc_fields = DocumentField.objects.filter(document=person.document).order_by('sort_order')

    main_data = []
    for doc_field in doc_fields:
        main_data.append({
            'label': doc_field.field.label,
            'code_name': doc_field.field.code_name,
            **_get_value_fer_fields(person, doc_field)
        })

    visa_data = [
        {
            'label': 'Визийн Дугаар',
            'code_name': 'eVisa Number',
            'value': person.number,
        },
        {
            'label': 'Визийн Төрөл Ангилал',
            'code_name': 'eVisa Category & Type',
            'value': person.visa.visa_kind.title,
        },
        {
            'label': 'Нэвтрэх Тоо',
            'code_name': 'Number of Entries',
            'value': str(person.visa.visa_kind.entry_kind),
        },
        {
            'label': 'Виз олгосон огноо',
            'code_name': 'Valid From',
            'value': now.strftime("%Y-%m-%d"),
        },
        {
            'label': 'Хүртэл хүчинтэй хугацаа',
            'code_name': 'Valid Until',
            'value': expiry.strftime("%Y-%m-%d"),
        },
        {
            'label': 'Байх хугацаа',
            'code_name': 'Duration of Stay',
            'value': str(person.visa.days_stay),
        }
    ]

    pdfmetrics.registerFont(TTFont('NotoR', f'{settings.STATIC_ROOT}/NotoSans-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('NotoB', f'{settings.STATIC_ROOT}/NotoSans-Bold.ttf'))

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setTitle('eVisa')

    pdf.setFont('NotoR', 18)
    pdf.drawCentredString(240, 790, 'МОНГОЛ УЛСЫН ЦАХИМ ВИЗ')

    pdf.setFont('NotoB', 18)
    pdf.drawCentredString(240, 760, 'Electronic Visa, Mongolia')

    pdf.setFont('NotoB', 60)
    pdf.drawString(400, 760, person.visa.visa_kind.code_name.upper())

    # Logo of Mongolian Government
    pdf.drawInlineImage(f'{settings.STATIC_ROOT}/logo.jpg', 20, 740, 80, 80)

    # QR Code
    _generate_qr_code(person.number)
    pdf.drawInlineImage(f'{settings.STATIC_ROOT}/qr.png', 496, 740, 80, 80)
    os.remove(f'{settings.STATIC_ROOT}/qr.png')

    # Line located bottom of head
    pdf.line(20, 730, 576, 730)

    y = 700
    for item in main_data:
        pdf.setFont('NotoR', 14)
        pdf.drawString(50, y, item['label'])
        pdf.setFont('NotoB', 12)
        pdf.drawString(50, y - 15, item['code_name'])
        pdf.setFont('NotoR', 14)
        pdf.drawString(250, y - 5, item['value'])
        pdf.line(50, y - 20, 400, y - 20)
        y = y - 35

    y = 300
    for item in visa_data:
        pdf.setFont('NotoR', 14)
        pdf.drawString(50, y, item['label'])
        pdf.setFont('NotoB', 12)
        pdf.drawString(50, y - 15, item['code_name'])
        pdf.setFont('NotoR', 14)
        pdf.drawString(250, y - 5, item['value'])
        pdf.line(50, y - 20, 400, y - 20)
        y = y - 35

    try:
        # Portrait Image
        pdf.drawInlineImage(f'{settings.MEDIA_ROOT}/{person.image_portrait}', 425, 550, 150, 150)
    except Exception:
        # Portrait Image
        pdf.drawInlineImage(f'{settings.STATIC_ROOT}/profile.png', 425, 550, 150, 150)

    # Old Mongolian alphabet
    pdf.drawInlineImage(f'{settings.STATIC_ROOT}/old.png', 425, 150, 150, 300)
    pdf.line(20, 60, 576, 60)
    pdf.setFillColorRGB(1, 0, 0)
    pdf.setFont('NotoB', 18)
    pdf.drawString(50, 40, 'Warning')
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont('NotoR', 12)
    pdf.drawString(
        50,
        20,
        'Please bring this notification with you and show it to a transport company for eVisa check.'
    )
    pdf.save()
    visa_pdf = buffer.getvalue()
    buffer.close()

    return visa_pdf
