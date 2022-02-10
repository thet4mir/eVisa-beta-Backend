import json
from functools import wraps

from django.http import HttpResponse
from django.http import HttpResponseBadRequest

from main.utils import JsonResponseFail


def login_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return HttpResponse(
            '{"is_success": false, "error": "login-required"}',
            status=401,
            content_type='application/json',
        )
    return wrap


def admin_required(func):
    @login_required
    @wraps(func)
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        return HttpResponse(
            '{"is_success": false, "error": "missing-permission"}',
            status=401,
            content_type='application/json',
        )
    return wrap


def json_decode_request_body(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        try:
            if request.body:
                request.body_json_decoded = json.loads(request.body)
            else:
                request.body_json_decoded = {}
        except Exception:
            return HttpResponseBadRequest('{"is_success": false}', content_type='application/json')

        return func(request, *args, **kwargs)
    return wrap


def responds_form_error(func):

    @wraps(func)
    def wrap(request, *args, **kwargs):

        func_gen = func(request, *args, **kwargs)

        forms = next(func_gen)
        is_valid = all((form.is_valid() for form in forms))

        if not is_valid:
            errors = dict()
            for form in forms:
                errors.update(form.errors)
            return JsonResponseFail({
                'form_errors': errors,
            })

        return next(func_gen)

    return wrap
