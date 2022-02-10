from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST, require_GET

from config.utils import ConfigCaptcha
from main.decorators import login_required, json_decode_request_body
from main.utils import JsonResponse

from .forms import PasswordChangeForm
from .forms import LoginForm


@require_POST
@json_decode_request_body
def login(request):

    if request.user.is_authenticated:
        return JsonResponse({'is_success': True})

    rsp = {
        'is_success': False,
    }

    form = LoginForm(request.body_json_decoded)
    if form.is_valid():

        user = auth.authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password'),
        )

        if user and user.is_superuser:
            auth.login(request, user)
            rsp['is_success'] = True
        else:
            rsp['errors'] = {
                'form': 'Хэрэглэгчийн нэр эсвэл нууц үг буруу байна!',
            }
    else:
        rsp['errors'] = form.errors

    return JsonResponse(rsp)


@require_POST
def logout(request):
    auth.logout(request)
    return HttpResponse('{"is_success": true}')


@require_GET
@ensure_csrf_cookie
def csrf_refresh(request):
    return HttpResponse('{"is_success": true}')


def csrf_failure(request, reason=""):
    return HttpResponseForbidden('{"error": "csrf-error"}')


@require_GET
def me(request):
    user = request.user

    current_user = {
        'is_authenticated': user.is_authenticated,
    }

    if current_user['is_authenticated']:
        current_user['email'] = request.user.email

    if request.user.is_superuser:
        current_user['is_superuser'] = True

    rsp = {
        'current_user': current_user,
        'is_success': True,
    }

    return JsonResponse(rsp)


@require_POST
@login_required
@json_decode_request_body
def change_password(request):

    rsp = {
        'is_success': False
    }
    payload = request.body_json_decoded
    form = PasswordChangeForm(request.user, payload)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        rsp['is_success'] = True
    else:
        rsp['form_errors'] = form.errors

    return JsonResponse(rsp)


@require_POST
def options(request):

    config_captcha = ConfigCaptcha()

    rsp = {
        'is_success': True,
        'recaptcha_site_key': (
            config_captcha.site_key
            if config_captcha.is_active
            else ''
        ),
    }

    return JsonResponse(rsp)
