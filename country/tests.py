from main.tests import BaseTestCase
from country.models import Country
from country.models import CountryLocale
from log.models import Log


class CountryPublic(BaseTestCase):

    def test_returns_active_only(self):
        """Returns only active countries"""

        # идэвхитэй
        country_mn = self.countries['mn']
        country_au = self.countries['au']
        country_ru = self.countries['ru']

        # идэвхигүй
        country_us = self.create_country(is_active=False)
        self.create_country_locale('en', country_us, name='United States', nationality='American')

        # default орчуулга ирэхийг шалгахын тулд устгана
        CountryLocale.objects.filter(country=country_ru, language=self.languages['mn']).delete()

        payload = {'language': 'mn'}
        rsp = self.post('/api/country/all/', payload)
        data = rsp.json()

        items = data.get('items')
        items_map = {item['id']: item for item in items}

        # идэвхитэй 3 хэл ирсэн эсэх
        self.assertEqual(len(items), 3, '3-н идэвхитэй хэл ирээгүй.')
        self.assertIn(country_mn.pk, items_map)
        self.assertIn(country_au.pk, items_map)
        self.assertIn(country_ru.pk, items_map)

        # Орчуулга зөв эсэх, байхгүй бол default хэлээр
        self.assertEqual(items_map[country_mn.pk]['name'], 'Монгол')
        self.assertEqual(items_map[country_au.pk]['name'], 'Австрали')
        self.assertEqual(items_map[country_ru.pk]['name'], 'Russia')


class CountrySecurity(BaseTestCase):

    def test_public_pages(self):
        self.assert_url_http200('/api/country/all/', {'language': 'mn'})

    def test_admin_pages_unauthorized(self):
        pk = self.countries['mn'].pk
        self.assert_url_http401('/api/country/admin/all/', {})
        self.assert_url_http401('/api/country/admin/create/', {'name': 'test'})
        self.assert_url_http401(f'/api/country/admin/{pk}/', {})
        self.assert_url_http401(f'/api/country/admin/{pk}/update/', {'name': 'test'})
        self.assert_url_http401(f'/api/country/admin/{pk}/toggle-active/', {'is_active': False})
        self.assert_url_http401(f'/api/country/admin/{pk}/delete/', {})


class CountryAdmin(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.login_superuser()

    def test_list(self):
        rsp = self.post('/api/country/admin/all/', {})
        data = rsp.json()
        items = data.get('items')
        items_map = {item['id']: item for item in items}

        def _assert_country(item, country):
            locale = country.locales.filter(language=self.languages['default']).first()
            self.assertEqual(item['is_active'], country.is_active)
            self.assertEqual(item['name'], locale.name)
            self.assertEqual(item['nationality'], locale.nationality)
            self.assertEqual(item['code_alpha2'], country.code_alpha2)
            self.assertEqual(item['code_alpha3'], country.code_alpha3)
            self.assertEqual(item['code_numeric'], country.code_numeric)
            self.assertIn('created_at', item)
            self.assertIn('updated_at', item)

        for country in self.countries.values():
            _assert_country(items_map[country.pk], country)

    def test_detail(self):
        country = self.create_country(is_active=False)
        self.create_country_locale('default', country, name='United States', nationality='American')

        rsp = self.post(f'/api/country/admin/{country.pk}/', {})
        item = rsp.json()['item']

        self.assertEqual(item['is_active'], False)
        self.assertEqual(item['name'], 'United States')
        self.assertEqual(item['nationality'], 'American')
        self.assertIn('created_at', item)
        self.assertIn('updated_at', item)

    def test_create(self):
        payload = {
            'is_active': True,
            'name': 'United States',
            'nationality': 'American',
            'code_alpha2': 'US',
            'code_alpha3': 'USA',
            'code_numeric': '840',
        }
        rsp = self.post('/api/country/admin/create/', payload)
        item = rsp.json()['item']

        logs = Log.objects.all()

        self.assertEqual(item['is_active'], True)
        self.assertEqual(item['name'], 'United States')
        self.assertEqual(item['nationality'], 'American')
        self.assertEqual(item['code_alpha2'], 'US')
        self.assertEqual(item['code_alpha3'], 'USA')
        self.assertEqual(item['code_numeric'], '840')
        self.assertIn('created_at', item)
        self.assertIn('updated_at', item)
        self.assertEqual(logs.count(), 2)

    def test_create_form_error(self):
        payload = {
            'is_active': True,
            'name': '',
            'nationality': '',
        }
        rsp = self.post('/api/country/admin/create/', payload, doAssert=False)
        self.assertEqual(rsp.status_code, 200)

        data = rsp.json()
        self.assertFalse(data['is_success'])

        num_errors = len(data['form_errors'].keys())
        self.assertEqual(num_errors, 5, 'Зөвхөн 5 алдаа гарна')
        self.assertIn('name', data['form_errors'])
        self.assertIn('nationality', data['form_errors'])
        self.assertIn('code_alpha2', data['form_errors'])
        self.assertIn('code_alpha3', data['form_errors'])
        self.assertIn('code_numeric', data['form_errors'])

    def test_update(self):
        country = self.countries['mn']
        payload = {
            'is_active': False,
            'name': 'changed_name',
            'nationality': 'changed_nationality',
            'code_alpha2': 'MN1',
            'code_alpha3': 'MNG1',
            'code_numeric': '840-1',
        }
        rsp = self.post(f'/api/country/admin/{country.pk}/update/', payload)
        item = rsp.json()['item']

        logs = Log.objects.all()

        self.assertEqual(item['is_active'], False)
        self.assertEqual(item['name'], 'changed_name')
        self.assertEqual(item['nationality'], 'changed_nationality')
        self.assertEqual(item['code_alpha2'], 'MN1')
        self.assertEqual(item['code_alpha3'], 'MNG1')
        self.assertEqual(item['code_numeric'], '840-1')
        self.assertIn('created_at', item)
        self.assertIn('updated_at', item)
        self.assertEqual(logs.count(), 2)

    def test_update_form_error(self):
        country = self.countries['mn']
        payload = {
            'is_active': False,
            'name': '',
            'nationality': '',
        }
        rsp = self.post(f'/api/country/admin/{country.pk}/update/', payload, doAssert=False)
        self.assertEqual(rsp.status_code, 200)

        data = rsp.json()
        self.assertFalse(data['is_success'])

        num_errors = len(data['form_errors'].keys())
        self.assertEqual(num_errors, 5, 'Зөвхөн 5 алдаа гарна')
        self.assertIn('name', data['form_errors'])
        self.assertIn('nationality', data['form_errors'])
        self.assertIn('code_alpha2', data['form_errors'])
        self.assertIn('code_alpha3', data['form_errors'])
        self.assertIn('code_numeric', data['form_errors'])

    def test_toggle_active(self):

        country = self.countries['ru']
        country.is_active = False
        country.save()

        payload = {'is_active': True}
        self.post('/api/country/admin/{}/toggle-active/'.format(country.pk), payload)

        logs = Log.objects.all()

        # идэвхитэй болгосон эсэх
        country_updated = Country.objects.get(pk=country.pk)
        self.assertTrue(country_updated.is_active, msg='Идэвхитэй болсон байх ёстой.')
        self.assertEqual(logs.count(), 1)

    def test_delete(self):
        pk = self.countries['ru'].pk
        self.post(f'/api/country/admin/{pk}/delete/', {})
        num_found = Country.objects.filter(pk=pk, deleted_at__isnull=True).count()
        self.assertEqual(num_found, 0, 'Улсыг устгаагүй байна.')
