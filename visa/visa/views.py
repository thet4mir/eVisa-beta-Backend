import random
import string
from django.contrib.auth import get_user_model
from main.utils import JsonResponse
from django.views.decorators.http import require_POST
from main.decorators import json_decode_request_body

from user.models import UserContact
from .forms import VisaForm
from visa.field.models import Field
from visa.document.models import DocumentField
from .models import Person, ValueDate, ValueText, ValueChoice


def _get_visa_display(visa):

    person_obj = Person.objects.filter(visa=visa)

    person_list = []
    for person in person_obj:
        doc_fields = DocumentField.objects.filter(document=person.document)
        person_values = []
        for doc_field in doc_fields:
            if doc_field.field.kind == Field.KIND_TEXT:
                value = ValueText.objects.get(document_field=doc_field, person=person).value
            elif doc_field.field.kind == Field.KIND_DATE:
                value = ValueDate.objects.get(document_field=doc_field, person=person).value
            elif doc_field.field.kind == Field.KIND_CHOICES:
                value = ValueChoice.objects.get(document_field=doc_field, person=person).value.code_name

            person_values.append({
                doc_field.field.code_name: value
            })

        person_list.append(person_values)

    return {
        'id': visa.id,
        'visa_kind': visa.visa_kind.id,
        'country': visa.country.code_alpha2,
        'date_of_arrival': visa.date_of_arrival,
        'days_stay': visa.days_stay,
        'days_valid': visa.days_valid,
        'entry_kind': visa.entry_kind,
        'fee_person': visa.fee_person,
        'created_by': visa.created_by.username,
        'created_at': visa.created_at,
        'person': person_list,
    }


def generate_password():
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_characters) for i in range(10))
    return password


def _create_user_from_value(payload):

    email = payload.get('email')
    User = get_user_model()
    check_user = User.objects.filter(email=email)

    if not check_user.count():
        user = User.objects.create_user(email, email, generate_password())

        user_contact = UserContact()
        user_contact.user = user
        user_contact.phone_no = payload.get('phone')
        user_contact.address = payload.get('address')
        user_contact.save()
    else:
        user = check_user.last()

    return user


@require_POST
@json_decode_request_body
def submit(request):

    payload = request.body_json_decoded
    rsp = {
        'is_success': False,
        'form_errors': {},
    }

    form_visa = VisaForm(payload, child_form_data=payload)

    if form_visa.is_valid():
        visa_kind = form_visa.instance.visa_kind
        form_visa.instance.days_stay = visa_kind.days_stay
        form_visa.instance.days_valid = visa_kind.days_valid
        form_visa.instance.entry_kind = visa_kind.entry_kind
        form_visa.instance.fee_person = visa_kind.fee_person
        form_visa.instance.created_by = _create_user_from_value(payload)
        visa = form_visa.save()

        rsp['is_success'] = True
        rsp['item'] = _get_visa_display(visa)
    else:
        rsp['form_errors'] = form_visa.errors

    return JsonResponse(rsp)
