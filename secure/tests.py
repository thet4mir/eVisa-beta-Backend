from main.tests import BaseTestCase

from django.contrib.auth import get_user_model


class SecureTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.login_superuser()

    def test_change_password_error(self):

        payload = {
            'old_password': 'superuser',
            'new_password1': 'mongol999#',
            'new_password2': 'mongol999',
        }

        rsp = self.post('/api/auth/change-password/', payload, doAssert=False)

        form_errors = rsp.json()['form_errors']
        self.assertIn('new_password2', form_errors)
        self.assertEqual(form_errors['new_password2'][0], 'Нууц үг таарсангүй!')

    def test_change_password(self):

        payload = {
            'old_password': 'superuser',
            'new_password1': 'mongol999#',
            'new_password2': 'mongol999#',
        }

        self.post('/api/auth/change-password/', payload, doAssert=False)

        User = get_user_model()
        user = User.objects.get(pk=self.superuser.pk)
        self.assertTrue(user.check_password('mongol999#'))

    def test_login_options(self):

        def _activate():
            self.configs['recaptcha_is_active'].value = 'yes'
            self.configs['recaptcha_is_active'].save()

        def _deactivate():
            self.configs['recaptcha_is_active'].value = 'no'
            self.configs['recaptcha_is_active'].save()

        def _fetch_site_key():
            rsp = self.post('/api/auth/login/options/', {})
            return rsp.json()['recaptcha_site_key']

        site_key = self.configs['recaptcha_site_key'].value

        # Inactive: recaptcha_site_key is empty
        _activate()
        self.assertEqual(_fetch_site_key(), site_key)

        # Active: recaptcha_site_key matched
        _deactivate()
        self.assertEqual(_fetch_site_key(), '')
