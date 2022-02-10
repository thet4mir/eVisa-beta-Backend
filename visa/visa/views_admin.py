import base64
from io import BytesIO
from PIL import Image
from django.conf import settings
from main.utils import JsonResponse
from datetime import timedelta
from django.utils import timezone
from .models import Person, ValueText, ValueDate, ValueChoice
from .forms import VisaFilterForm
from main.decorators import admin_required, json_decode_request_body
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .filter import VisaFilter
from visa.document.models import DocumentField
from visa.field.models import Field
from main.generate_pdf import GeneratePDF
from main.utils import send_pdf, send_mail
from django.db.models import Q
from config.models import Config
from visa.kind.models import VisaKindDiscount
from collections import Counter
from country.models import CountryLocale
from django.shortcuts import get_object_or_404
from main.utils import get_default_language_code_name
from user.models import UserContact


def _get_value_fer_fields(person, doc_field):

    if doc_field.field.kind == Field.KIND_TEXT:
        value_text = ValueText.objects.filter(person=person, document_field=doc_field)
        if value_text.count() != 0:
            return {'value': value_text.last().value}
        else:
            return {'value': ''}
    elif doc_field.field.kind == Field.KIND_DATE:
        value_date = ValueDate.objects.filter(person=person, document_field=doc_field)
        if value_date.count() != 0:
            return {'value': value_date.last().value}
        else:
            return {'value': ''}
    else:
        value_choice = ValueChoice.objects.filter(person=person, document_field=doc_field)
        if value_choice.count() != 0:
            return {'value': value_choice.last().value.label}
        else:
            return {'value': ''}


def _get_discounts_display(visa_kind):
    discount_list = []
    discounts = VisaKindDiscount.objects.filter(visa_kind=visa_kind)
    for discount in discounts:
        discount_list.append({
            'id': discount.id,
            'num_person': discount.num_person,
            'percent': discount.percent,
        })

    return discount_list


def _get_country_display(country):

    language_code_name = get_default_language_code_name()

    locale = get_object_or_404(
        CountryLocale,
        country=country,
        language__code_name=language_code_name,
    )

    return {
        'id': country.id,
        'name': locale.name,
    }


def _get_fee_exempt_country_display(visa_kind):

    return [
        _get_country_display(country)
        for country in visa_kind.fee_exempt_country.all()
    ]


def _get_person_display(person):

    user_info = UserContact.objects.filter(user=person.visa.created_by)
    doc_fields = DocumentField.objects.filter(document=person.document)

    field_json = []
    for doc_field in doc_fields:
        field_json.append({
            'id': doc_field.field.id,
            'label': doc_field.field.label,
            'code_name': doc_field.field.code_name,
            'sort_order': doc_field.sort_order,
            **_get_value_fer_fields(person, doc_field)
        })

    try:
        buffer_document = BytesIO()
        document = Image.open(f'{settings.MEDIA_ROOT}/{person.image_document.name}')
        document.save(buffer_document, format='JPEG')
        document_value = buffer_document.getvalue()

        document = 'data:image/jpeg;base64,' + base64.b64encode(document_value).decode()
    except Exception:
        document = ''

    try:
        buffer_portrait = BytesIO()
        portrait = Image.open(f'{settings.MEDIA_ROOT}/{person.image_portrait.name}')
        portrait.save(buffer_portrait, format='JPEG')
        portrait_value = buffer_portrait.getvalue()

        portrait = 'data:image/jpeg;base64,' + base64.b64encode(portrait_value).decode()
    except Exception:
        portrait = ''

    return {
        'id': person.id,
        'number': person.number,
        'status': person.status,
        'document': person.document.name,
        'entry_kind': person.visa.entry_kind,
        'image_document': document,
        'image_portrait': portrait,
        'fee_exempt_countries': _get_fee_exempt_country_display(person.visa.visa_kind),
        'discount_list': _get_discounts_display(person.visa.visa_kind),
        'days_stay': person.visa.days_stay,
        'days_valid': person.visa.days_valid,
        'created_by': person.visa.created_by.username,
        'phone_no': user_info.last().phone_no if user_info.count() else '',
        'address': user_info.last().address if user_info.count() else '',
        'updated_by': person.updated_by.username if person.updated_by else None,
        'visa_kind': person.visa.visa_kind.title,
        'country': person.visa.country.get_default_name(),
        'fee_person': person.visa.fee_person,
        'date_of_arrival': person.visa.date_of_arrival,
        'fields': field_json,
        'created_at': person.created_at,
        'updated_at': person.updated_at,
        'dead_line': ((person.created_at + timedelta(days=3)) - timezone.now()).total_seconds()
    }


def _get_people_list_display(person):

    name_value = ValueText.objects.filter(person=person, document_field__field__code_name='name')
    surname_value = ValueText.objects.filter(person=person, document_field__field__code_name='surname')
    name = name_value.last().value if name_value.count() != 0 else ''
    surname = surname_value.last().value if surname_value.count() != 0 else ''

    dead_line_total_seconds = ((person.created_at + timedelta(days=3)) - timezone.now()).total_seconds()
    dead_line = dead_line_total_seconds if person.status == Person.STATUS_NEW else 260000

    return {
        'id': person.id,
        'name': name,
        'surname': surname,
        'number': person.number,
        'status': person.status,
        'created_by': person.visa.created_by.email,
        'updated_by': person.updated_by.email if person.updated_by else None,
        'visa_kind': person.visa.visa_kind.title,
        'fee_person': person.visa.fee_person,
        'country': person.visa.country.get_default_name(),
        'created_at': person.created_at,
        'updated_at': person.updated_at,
        'dead_line': dead_line
    }


@require_POST
@admin_required
def details(request, pk):

    person = Person.objects.get(pk=pk)

    rsp = {
        'is_success': True,
        'item': _get_person_display(person)
    }

    return JsonResponse(rsp)


@require_POST
@admin_required
@json_decode_request_body
def list(request):

    payload = request.body_json_decoded

    text = payload.get('text')
    country = payload.get('country')
    start_date = payload.get('start_date')
    end_date = payload.get('end_date')
    status = payload.get('status')
    sort_direction = payload.get('sort_direction')
    sort_key = payload.get('sort_key')

    people = Person.objects.all().order_by('-visa__created_at')

    if text or country or start_date or end_date or status:
        filter_form = VisaFilterForm(payload)
    else:
        filter_form = VisaFilterForm()

    filtered_people_list = VisaFilter(people, filter_form).filter()

    sort_options = {
        'country': 'visa__country',
        'number': 'number',
        'status': 'status',
        'created_at': 'created_at',
    }

    if sort_key in sort_options:
        order = (
            (sort_direction == 'desc' and '-' or '')
            + sort_options[sort_key]
        )
        filtered_people_list = filtered_people_list.order_by(order)

    people_list = [
        _get_people_list_display(person)
        for person in filtered_people_list
    ]

    count = Counter(person['status'] for person in people_list)
    total_new = count[Person.STATUS_NEW]
    total_approve = count[Person.STATUS_APPROVE]
    total_decline = count[Person.STATUS_DECLINE]

    people_list.sort(key=lambda x: x.get('dead_line'))

    paginator = Paginator(people_list, 25)
    page = payload.get('page', 1)
    result = paginator.get_page(page)

    rsp = {
        'is_success': True,
        'results': result.object_list,
        'total_page': paginator.num_pages,
        'page': result.number,
        'total_record': paginator.count,
        'total_new': total_new,
        'total_approve': total_approve,
        'total_decline': total_decline,
    }

    return JsonResponse(rsp)


def _get_email_body_subject(lang, kind):

    if kind == 'success':
        body = Config.objects.filter(
            Q(name__icontains='success') &
            Q(name__icontains='body') &
            Q(name__icontains=lang)
        )
        subject = Config.objects.filter(
            Q(name__icontains='success') &
            Q(name__icontains='subject') &
            Q(name__icontains=lang)
        )
    elif kind == 'reject':
        body = Config.objects.filter(
            Q(name__icontains='reject') &
            Q(name__icontains='body') &
            Q(name__icontains=lang)
        )
        subject = Config.objects.filter(
            Q(name__icontains='reject') &
            Q(name__icontains='subject') &
            Q(name__icontains=lang)
        )

    if body.count() != 0:
        body_text = body.last().value
    else:
        if kind == 'success':
            body_text = 'Mongolian Visa has been accepted.'
        elif kind == 'reject':
            body_text = 'Mongolian Visa has been rejected.'

    if subject.count() != 0:
        subject_text = subject.last().value
    else:
        if kind == 'success':
            subject_text = 'We are happy to inform you that your "Visa Application" has been accepted.'
        elif kind == 'reject':
            subject_text = 'We are sorry to inform you that your "Visa Application" has been rejected.'

    return {
        'body': body_text,
        'subject': subject_text,
    }


@require_POST
@json_decode_request_body
@admin_required
def approve(request, pk):

    payload = request.body_json_decoded
    person = Person.objects.get(pk=pk)

    if not person.updated_by:
        pdf = GeneratePDF(person)

        mail_config = _get_email_body_subject(payload.get('language'), 'success')
        body = mail_config['body']
        subject = mail_config['subject']
        send_pdf(
            person.visa.created_by.email,
            subject,
            '',
            body,
            pdf
        )
        person.status = Person.STATUS_APPROVE
        person.updated_by = request.user
        person.save()

    rsp = {
        'is_success': True,
        'item': _get_person_display(person)
    }

    return JsonResponse(rsp)


@require_POST
@json_decode_request_body
@admin_required
def decline(request, pk):

    payload = request.body_json_decoded
    person = Person.objects.get(pk=pk)

    mail_config = _get_email_body_subject(payload.get('language'), 'reject')
    body = mail_config['body']
    subject = mail_config['subject']
    send_mail(
        person.visa.created_by.email,
        subject,
        '',
        body
    )

    if not person.updated_by:
        person.status = Person.STATUS_DECLINE
        person.updated_by = request.user
        person.save()

    rsp = {
        'is_success': True,
        'item': _get_person_display(person)
    }

    return JsonResponse(rsp)
