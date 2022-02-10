import requests

from django.core.exceptions import ValidationError

from config.utils import ConfigCaptcha


def validate_captcha(g_recaptcha_response):

    config_captcha = ConfigCaptcha()

    if config_captcha.is_active:
        return

    has_missing_param = not all([
        config_captcha.verify_url,
        config_captcha.secret_key,
        config_captcha.site_key,
    ])

    if has_missing_param:
        # TODO notify admins
        raise ValidationError('Captcha verification failed!')

    data = {
        'secret': config_captcha.secret_key,
        'response': g_recaptcha_response,
    }

    try:
        r = requests.post(config_captcha.verify_url, data=data, timeout=10)
        is_verify_success = r.json()['success']
    except Exception:
        raise ValidationError('Cannot verify captcha at this time!')

    if not is_verify_success:
        raise ValidationError('Invalid captcha. Please try again!')
