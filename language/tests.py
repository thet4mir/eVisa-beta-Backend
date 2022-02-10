from main.tests import BaseTestCase
from language.models import Language


class LanguagePublic(BaseTestCase):

    def test_public_list(self):

        rsp = self.get('/api/language/all/')
        data = rsp.json()
        items = data.get('items')
        items_map = {item['id']: item for item in items}

        def _assert_language(item, lang):
            self.assertEqual(item['code_name'], lang.code_name)
            self.assertEqual(item['name_local'], lang.name_local)
            self.assertEqual(item['is_default'], lang.is_default)

        for lang in self.languages.values():
            _assert_language(items_map[lang.pk], lang)


class LanguageSecurity(BaseTestCase):

    def test_public_pages(self):
        self.assert_url_http200('/api/language/all/', '', method='GET')

    def test_admin_pages_unauthorized(self):
        pk = self.languages['mn'].pk
        self.assert_url_http401('/api/language/admin/all/', {})
        self.assert_url_http401('/api/language/admin/create/', {'name': 'test'})
        self.assert_url_http401(f'/api/language/admin/{pk}/toggle-active/', {})
        self.assert_url_http401(f'/api/language/admin/{pk}/set-default/', {})
        self.assert_url_http401(f'/api/language/admin/{pk}/update/', {'name': 'test'})
        self.assert_url_http401(f'/api/language/admin/{pk}/', {})
        self.assert_url_http401(f'/api/language/admin/{pk}/delete/', {})


class LanguageAdmin(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.login_superuser()

    def test_language_active_error(self):

        lang = self.languages['en']
        rsp = self.post(f'/api/language/admin/{lang.pk}/set-default/', {}, doAssert=False)

        data = rsp.json()['errors']
        self.assertEqual(data, 'Идэвхигүй хэлийг default хэл болгох боломжгүй!')

    def test_list(self):
        rsp = self.post('/api/language/admin/all/', {})
        data = rsp.json()
        items = data.get('items')
        items_map = {item['id']: item for item in items}

        def _assert_language(item, lang):
            self.assertEqual(item['name'], lang.name)
            self.assertEqual(item['code_name'], lang.code_name)
            self.assertEqual(item['name_local'], lang.name_local)
            self.assertEqual(item['is_active'], lang.is_active)
            self.assertEqual(item['is_default'], lang.is_default)
            self.assertIn('created_at', item)
            self.assertIn('updated_at', item)

        for lang in self.languages.values():
            _assert_language(items_map[lang.pk], lang)

    def test_details(self):
        lang = self.languages['en']

        rsp = self.post(f'/api/language/admin/{lang.id}/', {})
        item = rsp.json()['item']

        self.assertEqual(item['name'], lang.name)
        self.assertEqual(item['code_name'], lang.code_name)
        self.assertEqual(item['name_local'], lang.name_local)
        self.assertEqual(item['is_active'], lang.is_active)
        self.assertEqual(item['is_default'], lang.is_default)
        self.assertIn('created_at', item)
        self.assertIn('updated_at', item)

    def test_create_success(self):
        payload = {
            'name': 'Англи хэл',
            'code_name': 'en',
            'name_local': 'English',
            'is_active': True,
            'is_default': False
        }

        rsp = self.post('/api/language/admin/create/', payload)
        item = rsp.json()['item']

        self.assertEqual(item['name'], 'Англи хэл')
        self.assertEqual(item['code_name'], 'en')
        self.assertEqual(item['name_local'], 'English')
        self.assertEqual(item['is_active'], True)
        self.assertEqual(item['is_default'], False)
        self.assertIn('created_at', item)
        self.assertIn('updated_at', item)

    def test_create_fail(self):

        payload = {
            'name': '',
            'code_name': '',
            'name_local': '',
            'is_active': True,
            'is_default': False
        }

        rsp = self.post('/api/language/admin/create/', payload, doAssert=False)
        errors = rsp.json()['form_errors']

        self.assertIn('name', errors)
        self.assertIn('code_name', errors)
        self.assertIn('name_local', errors)

    def test_toggle_active(self):

        lang = Language.objects.filter(is_active=True, is_default=False).first()

        is_active_new = not lang.is_active

        payload = {'is_active': is_active_new}
        self.post(f'/api/language/admin/{lang.pk}/toggle-active/', payload)

        lang_updated = Language.objects.get(pk=lang.pk)
        self.assertEqual(lang_updated.is_active, is_active_new, msg='Идэвхитэй болсон байх ёстой.')

    def test_toggle_active_fail(self):

        qs = Language.objects.filter(
            is_active=True,
            is_default=True,
        )
        lang = qs.first()

        is_active_new = not lang.is_active

        payload = {'is_active': is_active_new}
        rsp = self.post(f'/api/language/admin/{lang.pk}/toggle-active/', payload, doAssert=False)
        data = rsp.json()

        self.assertEqual(data['error'], 'Үндсэн хэлийг идэвхигүй болгох боломжгүй байна!')

    def test_set_default(self):

        lang = self.languages['mn']

        payload = {'is_default': True}
        self.post(f'/api/language/admin/{lang.pk}/set-default/', payload)

        lang_updated = Language.objects.get(pk=lang.pk)
        self.assertTrue(lang_updated.is_default, msg='Идэвхитэй болсон байх ёстой.')

    def test_update_success(self):
        lang = self.languages['ru']
        payload = {
            'name': 'changed_name',
            'code_name': 'ru1',
            'name_local': 'changed_name_local',
            'is_active': False,
            'is_default': True,
        }
        rsp = self.post(f'/api/language/admin/{lang.pk}/update/', payload)
        item = rsp.json()['item']

        lang_updated = Language.objects.get(pk=lang.pk)
        self.assertEqual(item['name'], lang_updated.name)
        self.assertEqual(item['code_name'], lang_updated.code_name)
        self.assertEqual(item['name_local'], lang_updated.name_local)
        self.assertIs(item['is_active'], lang_updated.is_active)
        self.assertIs(item['is_default'], lang_updated.is_default)

    def test_update_fail(self):
        lang = self.languages['ru']
        payload = {
            'name': '',
            'code_name': '',
            'name_local': '',
            'is_active': False,
            'is_default': True,
        }
        rsp = self.post(f'/api/language/admin/{lang.pk}/update/', payload, doAssert=False)
        errors = rsp.json()['form_errors']

        self.assertIn('name', errors)
        self.assertIn('code_name', errors)
        self.assertIn('name_local', errors)

    def test_delete(self):
        lang = self.create_language(
            name='Голланд',
            code_name='nl',
            name_local='Nederlands',
            is_active=True,
            is_default=False,
        )
        self.post(f'/api/language/admin/{lang.pk}/delete/', {})

        is_found = Language.objects.filter(pk=lang.pk).exists()

        self.assertFalse(is_found, 'Энэ хэлийг устгаагүй байна!')

    def test_delete_fail(self):
        lang = self.create_language(
            name='Голланд',
            code_name='nl',
            name_local='Nederlands',
            is_active=True,
            is_default=True,
        )
        rsp = self.post(f'/api/language/admin/{lang.pk}/delete/', {}, doAssert=False)
        data = rsp.json()
        is_found = Language.objects.filter(pk=lang.pk).exists()

        self.assertFalse(data['is_success'])
        self.assertEqual(data['error'], 'Үндсэн хэлийг устгах боломжгүй байна!')
        self.assertTrue(is_found)
