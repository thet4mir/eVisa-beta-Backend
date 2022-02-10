import secrets
import time

from django.conf import settings

from main.decorators import admin_required
from main.decorators import json_decode_request_body
from main.utils import JsonResponse

from .forms import GenerateForm
from .models import VisaPersonNumber


class Timer():

    def __init__(self, seconds):
        self.ts_end = time.time() + seconds

    def has_finished(self):
        return time.time() > self.ts_end


def _exclude_existing(numbers):
    qs = VisaPersonNumber.objects.filter(id__in=numbers)
    numbers_existing = qs.values_list('id', flat=True)

    return set(numbers) - set(numbers_existing)


def _generate_numbers(length, amount):

    timer = Timer(settings.GENERATE_VISA_PERSON_NUMBER_TIMEOUT)
    num_left = amount
    batch_size = settings.GENERATE_VISA_PERSON_NUMBER_BATCH_SIZE
    chars = VisaPersonNumber.ID_CHARS

    while True:

        numbers = [
            ''.join(secrets.choice(chars) for i in range(length))
            for i in range(min(num_left, batch_size))
        ]
        numbers = _exclude_existing(numbers)

        VisaPersonNumber.objects.bulk_create([
            VisaPersonNumber(id=number, length=length, is_used=False)
            for number in numbers
        ])

        num_left -= len(numbers)

        if num_left <= 0 or timer.has_finished():
            break

    num_created = amount - num_left

    return num_created


@admin_required
@json_decode_request_body
def generate(request):

    form = GenerateForm(request.body_json_decoded)

    rsp = {
        'is_success': False,
    }

    if form.is_valid():
        length = form.cleaned_data['length']
        amount = form.cleaned_data['amount']
        num_created = _generate_numbers(length, amount)
        rsp['is_success'] = True
        rsp['amount'] = num_created
    else:
        rsp['form_errors'] = form.errors

    return JsonResponse(rsp)


@admin_required
def statistics(request):

    qs = VisaPersonNumber.objects.all()

    num_used = qs.filter(is_used=True).count()
    num_unused = qs.filter(is_used=False).count()
    num_total = num_used + num_unused

    rsp = {
        'is_success': True,
        'used': num_used,
        'unused': num_unused,
        'total': num_total,
    }

    return JsonResponse(rsp)
