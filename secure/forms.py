from django import forms
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm

from config.utils import ConfigCaptcha
from main.forms import BaseForm
from main.validators import validate_captcha
from user.forms import PasswordValidationMixin


class PasswordChangeForm(PasswordValidationMixin, DjangoPasswordChangeForm):

    PASSWORD2_FIELD = 'new_password2'


class LoginForm(BaseForm):

    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)
    g_recaptcha_response = forms.CharField(validators=[validate_captcha], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        config_captcha = ConfigCaptcha()
        self.fields['g_recaptcha_response'].required = config_captcha.is_active
