from django.apps import apps


class BaseConfig():

    def get_configs_by_name(self, names):

        Config = apps.get_model('config', 'Config')

        config_dict = {
            conf.name: conf.value
            for conf in Config.objects.filter(name__in=names)
        }

        values = [
            config_dict.get(name)
            for name in names
        ]

        return values


class ConfigEmailResponse(BaseConfig):

    email_visa_success_body_en = ''
    email_visa_success_subject_en = ''

    def __init__(self):

        (
            self.email_visa_success_body_en,
            self.email_visa_success_subject_en,

        ) = self.get_configs_by_name([

            'email_visa_success_body_en',
            'email_visa_success_subject_en',

        ])


class ConfigEmail(BaseConfig):

    host = ''
    port = ''
    user = ''
    password = ''

    def __init__(self):

        (
            self.host,
            self.port,
            self.user,
            self.password,

        ) = self.get_configs_by_name([

            'email_host',
            'email_port',
            'email_user',
            'email_password',

        ])


class ConfigCaptcha(BaseConfig):

    is_active = ''
    site_key = ''
    secret_key = ''
    verify_url = ''

    def __init__(self):

        (

            self.is_active,
            self.site_key,
            self.secret_key,
            self.verify_url,

        ) = self.get_configs_by_name([

            'recaptcha_is_active',
            'recaptcha_site_key',
            'recaptcha_secret_key',
            'recaptcha_verify_url',

        ])

        self.is_active = self.is_active == 'yes'
