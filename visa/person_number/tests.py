from main.tests import BaseTestCase

from .models import VisaPersonNumber


class VisaPersonNumberSecurity(BaseTestCase):

    def test_admin_pages_unauthorized(self):
        self.assert_url_http401('/api/visa/person-number/admin/generate/', {})
        self.assert_url_http401('/api/visa/person-number/admin/statistics/', {})


class VisaPersonNumberAdmin(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.login_superuser()

    def test_generate_fail(self):
        payload = {}
        rsp = self.post('/api/visa/person-number/admin/generate/', payload, doAssert=False)
        data = rsp.json()

        self.assertFalse(data['is_success'])
        self.assertIn('form_errors', data)
        self.assertIn('amount', data['form_errors'])
        self.assertIn('length', data['form_errors'])

    def test_generate_success(self):

        def _get_count(length):
            return VisaPersonNumber.objects.filter(length=8, is_used=False).count()

        payload = {
            'length': 8,
            'amount': 11,
        }

        num_before = _get_count(payload['length'])
        with self.settings(
            GENERATE_VISA_PERSON_NUMBER_TIMEOUT=.4,
            GENERATE_VISA_PERSON_NUMBER_BATCH_SIZE=5,
        ):
            rsp = self.post('/api/visa/person-number/admin/generate/', payload)
        data = rsp.json()
        num_after = _get_count(payload['length'])

        self.assertEqual(data['amount'], payload['amount'])
        self.assertEqual(num_before + data['amount'], num_after)

    def test_statistics(self):

        VisaPersonNumber.objects.create(id='0789ACDE', length=8, is_used=False)
        VisaPersonNumber.objects.create(id='1789ACDE', length=8, is_used=True)

        num_used = VisaPersonNumber.objects.filter(is_used=True).count()
        num_unused = VisaPersonNumber.objects.filter(is_used=False).count()
        num_total = num_used + num_unused

        rsp = self.post('/api/visa/person-number/admin/statistics/', {})
        data = rsp.json()

        self.assertEqual(data['used'], num_used)
        self.assertEqual(data['unused'], num_unused)
        self.assertEqual(data['total'], num_total)
