import base64
import datetime

from io import BytesIO
from PIL import Image
from django.apps import apps
from django.core import mail
from django.core.cache import cache
from django.core.mail import send_mail as django_send_mail
from django.core.mail import EmailMessage
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Prefetch
from django.http import JsonResponse as DjangoJsonResponse
from django.core.files.uploadedfile import SimpleUploadedFile
from config.utils import ConfigEmail


def pill_resize_img(img, w, h):

    bytes_img_dst = BytesIO()

    image = Image.open(img)

    if img.height > h or img.width > w:
        image.thumbnail([w, h])

    image.save(bytes_img_dst, 'JPEG')
    return SimpleUploadedFile(img.name, bytes_img_dst.getvalue(), content_type='iamge/jpeg')


def create_simple_uploaded_obj(img):

    try:
        img_byte = base64.b64decode(img)
    except Exception:
        return None

    if img_byte:
        simple_upload_obj = SimpleUploadedFile(
            'tmp.jpeg',
            img_byte,
            content_type='image/jpeg'
        )
        return simple_upload_obj
    else:
        return None


def send_pdf(mail_to, subject, body_plain, body, pdf):

    config_email = ConfigEmail()
    connection = mail.get_connection(
        username=config_email.user,
        password=config_email.password,
        port=config_email.port,
        host=config_email.host,
        use_ssl=True,
        fail_silently=False,
    )

    email = EmailMessage(
        subject,
        body,
        config_email.user,
        [mail_to],
        connection=connection,
    )
    email.content_subtype = 'html'
    email.attach('visa.pdf', pdf, 'application/pdf')
    is_success = email.send()

    return is_success == 1


def send_mail(mail_to, subject, body_plain, body):

    config_email = ConfigEmail()

    connection = mail.get_connection(
        username=config_email.user,
        password=config_email.password,
        port=config_email.port,
        host=config_email.host,
        use_ssl=True,
        fail_silently=False,
    )

    is_success = django_send_mail(
        subject,
        body_plain,
        config_email.user,
        [mail_to],
        connection=connection,
        html_message=body,
    )
    return is_success == 1


def get_default_language_code_name():
    cache_key = 'g:default_language_code_name'
    rval = cache.get(cache_key)
    if not rval:
        Language = apps.get_model('language', 'Language')
        language = Language.objects.get(is_default=1, is_active=True)
        rval = language.code_name
        cache.set(cache_key, rval, 300)
    return rval


def prefetch_locale(model, lang_code):
    lang_code_default = get_default_language_code_name()

    qs = model.objects.filter(
        language__code_name__in=[lang_code, lang_code_default],
        language__is_active=True,
    )
    qs = qs.order_by('language__is_default')
    return Prefetch('locales', queryset=qs)


class JSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        else:
            return super().default(o)


class JsonResponse(DjangoJsonResponse):
    def __init__(self, *args, **kwargs):
        kwargs['encoder'] = JSONEncoder
        return super().__init__(*args, **kwargs)


class JsonResponseSuccess(JsonResponse):
    def __init__(self, data, *args, **kwargs):
        data = {**data, 'is_success': True}
        return super().__init__(data, *args, **kwargs)


class JsonResponseFail(JsonResponse):
    def __init__(self, data, *args, **kwargs):
        data = {**data, 'is_success': False}
        return super().__init__(data, *args, **kwargs)
