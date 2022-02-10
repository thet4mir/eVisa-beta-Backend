from django.contrib.auth import get_user_model
from main.tests import BaseTestCase


class UserAdmin(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.login_superuser()

    def test_user_update_with_password_mismatch(self):

        payload = {
            'email': 'newemail@email.com',
            'first_name': 'newfirt_name',
            'last_name': 'newlast_name',
            'is_superuser': 1,
            'password1': 'sdfsdfsd',
            'password2': 'sdfsdfsd1',
        }

        rsp = self.post(f'/api/user/{self.superuser.pk}/update/', payload, doAssert=False)

        errors = rsp.json()['form_errors']
        self.assertEqual(len(errors), 1)
        self.assertIn('password2', errors)

    def test_user_update_with_error(self):
        payload = {
            'email': 'newemail@email.com',
            'first_name': 'newfirt_name',
            'last_name': 'newlast_name',
            'is_superuser': 1,
            'password1': 'sdfsdfsd',
            'password2': '',
        }

        rsp = self.post(f'/api/user/{self.superuser.pk}/update/', payload, doAssert=False)

        data = rsp.json()['form_errors']
        self.assertEqual(len(data), 1)

    def test_user_update_without_password(self):
        payload = {
            'email': 'newemail@email.com',
            'first_name': 'newfirt_name',
            'last_name': 'newlast_name',
            'is_superuser': True,
            'password1': '',
            'password2': '',
        }

        self.post(f'/api/user/{self.superuser.pk}/update/', payload)
        User = get_user_model()
        user = User.objects.get(pk=self.superuser.pk)

        self.assertEqual(user.email, 'newemail@email.com')
        self.assertEqual(user.first_name, 'newfirt_name')
        self.assertEqual(user.last_name, 'newlast_name')
        self.assertTrue(user.is_superuser)

    def test_user_update_with_password(self):
        payload = {
            'email': 'newemail@email.com',
            'first_name': 'newfirt_name',
            'last_name': 'newlast_name',
            'is_superuser': True,
            'password1': 'mongol99#',
            'password2': 'mongol99#',
        }

        self.post(f'/api/user/{self.superuser.pk}/update/', payload, doAssert=False)

        User = get_user_model()
        user = User.objects.get(pk=self.superuser.pk)
        self.assertEqual(user.email, 'newemail@email.com')
        self.assertEqual(user.first_name, 'newfirt_name')
        self.assertEqual(user.last_name, 'newlast_name')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password('mongol99#'))

    def test_toggle_active(self):

        user = self.superuser

        rsp = self.post(f'/api/user/{user.id}/toggle-active/', {}, doAssert=False)
        data = rsp.json()

        self.assertFalse(data['is_success'])
        self.assertEqual(data['form_errors']['is_active'][0], 'Өөрийгөө идэвхигүй болгох боломжгүй байна!')

        User = get_user_model()
        user = User.objects.create_user(
            'testsuperuser',
            'testuser@gmail.com',
            'testsuperuser',
            is_superuser=True,
            is_active=False
        )

        self.post(f'/api/user/{user.id}/toggle-active/', {})

        user_updated = User.objects.get(pk=user.id)
        self.assertTrue(user_updated.is_active)
