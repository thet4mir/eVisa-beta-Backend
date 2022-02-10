from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from main.decorators import admin_required
from main.decorators import responds_form_error
from main.decorators import json_decode_request_body
from main.utils import JsonResponse
from main.utils import JsonResponseSuccess

from .forms import UserCreateForm
from .forms import UserUpdateForm
from .forms import AdminPasswordChangeForm
from .forms import UserToggleActiveForm


def _user_or_404(pk):
    qs = get_user_model().objects
    return get_object_or_404(qs, pk=pk)


def _get_user_display(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_superuser': user.is_superuser,
        'is_active': user.is_active,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
        'updated_at': user.updated_at,
    }


@require_POST
@admin_required
def all(request):
    users = get_user_model().objects.all()

    users_display = [
        _get_user_display(user)
        for user in users
    ]

    return JsonResponseSuccess({
        'items': users_display,
    })


@require_POST
@admin_required
@json_decode_request_body
@responds_form_error
def create(request):

    payload = request.body_json_decoded
    payload['username'] = payload.get('email')
    form = UserCreateForm(payload)

    yield [form]  # validates with decorator

    user = form.save()

    yield JsonResponseSuccess({
        'item': _get_user_display(user)
    })


@require_POST
@admin_required
@json_decode_request_body
def update(request, pk):

    rsp = {
        'is_success': False,
        'item': {}
    }
    payload = request.body_json_decoded

    User = get_user_model()
    user = get_object_or_404(User, pk=pk, is_deleted=False)
    form1 = UserUpdateForm(payload)
    form2 = AdminPasswordChangeForm(user, payload)
    if form1.is_valid():

        if payload.get('password1'):
            if form2.is_valid():
                form2.save()
            else:
                rsp['form_errors'] = form2.errors
                return JsonResponse(rsp)

        user.email = payload.get('email')
        user.username = payload.get('email')
        user.first_name = payload.get('first_name')
        user.last_name = payload.get('last_name')
        user.is_superuser = payload.get('is_superuser') is True
        user.save()

        rsp['item'] = _get_user_display(user)
        rsp['is_success'] = True
    else:
        rsp['form_errors'] = form1.errors

    return JsonResponse(rsp)


@require_POST
@admin_required
def remove(request, pk):

    user = _user_or_404(pk)
    user.is_deleted = True
    user.save()

    return JsonResponseSuccess({})


@require_POST
@admin_required
def details(request, pk):

    user = _user_or_404(pk)

    return JsonResponseSuccess({
        'item': _get_user_display(user)
    })


@require_POST
@admin_required
@responds_form_error
def toggle_active(request, pk):

    user = _user_or_404(pk)
    payload = {'is_active': not user.is_active}
    form = UserToggleActiveForm(request, payload, instance=user)

    yield [form]  # validates with decorator

    form.save()

    yield JsonResponseSuccess({})
