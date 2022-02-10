from django.core import mail

from main.tests import BaseTestCase


class ConfigSecurity(BaseTestCase):

    def test_admin_pages_unauthorized(self):
        self.assert_url_http401('/api/config/admin/all/', {})

        payload = {
            'name': 'name1',
            'value': 'val1',
        }
        self.assert_url_http401('/api/config/admin/save/', payload)

        payload = {
            'send_to': 'user@example.com',
            'subject': 'subject1',
            'body': 'body1',
        }
        self.assert_url_http401('/api/config/admin/test-send-mail/', payload)


class ConfigAdmin(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.login_superuser()

    def test_list(self):
        rsp = self.post('/api/config/admin/all/', {})
        data = rsp.json()
        items = data.get('configs')
        items_map = {item['name']: item for item in items}

        def _assert_config(item, config):
            self.assertEqual(item['value'], config.value)
            self.assertIn('created_at', item)
            self.assertIn('updated_at', item)

        self.assertEqual(len(items), 8)
        for name, config in self.configs.items():
            _assert_config(items_map[name], config)

    def test_save_fail(self):

        # create new
        payload = {'name': '', 'value': ''}
        rsp = self.post('/api/config/admin/save/', payload, doAssert=False)
        data = rsp.json()

        self.assertFalse(data['is_success'])
        self.assertIn('name', data['errors'])
        self.assertIn('value', data['errors'])
        self.assertIsInstance(data['errors']['name'], list)
        self.assertIsInstance(data['errors']['value'], list)

        # update existing
        config = self.configs['email_host']
        payload = {'name': config.name, 'value': ''}
        rsp = self.post('/api/config/admin/save/', payload, doAssert=False)
        data = rsp.json()

        self.assertFalse(data['is_success'])
        self.assertIn('value', data['errors'])
        self.assertIsInstance(data['errors']['value'], list)

    def test_save_success(self):

        # create new
        payload = {
            'name': 'name1',
            'value': 'value1',
        }
        rsp = self.post('/api/config/admin/save/', payload, doAssert=False)
        data = rsp.json()

        self.assertEqual(rsp.status_code, 200)
        self.assertTrue(data.get('is_success'))

        # update existing
        config = self.configs['email_host']
        payload = {
            'name': config.name,
            'value': 'modified_value',
        }
        rsp = self.post('/api/config/admin/save/', payload, doAssert=False)
        data = rsp.json()

        self.assertEqual(rsp.status_code, 200)
        self.assertTrue(data.get('is_success'))

    def test_send_mail(self):

        send_to, subject, body = "user@example.com", "subject1", "body1"

        payload = {
            "send_to": send_to,
            "subject": subject,
            "body": body,
        }

        self.post('/api/config/admin/test-send-mail/', payload)

        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertEqual(email.subject, subject)

        self.assertEqual(len(email.to), 1)
        self.assertEqual(email.to[0], send_to)

        self.assertEqual(len(email.alternatives), 1)
        self.assertEqual(email.alternatives[0][0], body)
        self.assertEqual(email.alternatives[0][1], 'text/html')

        sender = self.configs['email_user'].value
        self.assertEqual(email.from_email, sender)
