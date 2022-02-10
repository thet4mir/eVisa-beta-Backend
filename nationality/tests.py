from main.tests import BaseTestCase
from .models import Nationality, NationalityLocale


class BaseNationality(BaseTestCase):

    def create_nationality(self, country_code_name, name_mn, name_en, is_active):

        def _create_locale(lang_code_name, nationality, name):
            if name:
                NationalityLocale.objects.create(
                    language=self.languages[lang_code_name],
                    nationality=nationality,
                    name=name
                )
        nationality = Nationality.objects.create(
            country=self.countries[country_code_name],
            is_active=is_active
        )
        _create_locale('mn', nationality, name_mn)
        _create_locale('en', nationality, name_en)

        return nationality


class NationalityAdmin(BaseNationality):

    def setUp(self):
        super().setUp()
        self.login_superuser()

    def test_all_nationality(self):

        nation_ru = self.create_nationality('ru', 'Орос', 'Russian', True)
        nation_au = self.create_nationality('au', 'Австрали', 'Australian', False)

        response = self.post('/api/nationality/admin/all/', {})

        data = response.json()
        items = data.get('items')

        self.assertEqual(len(items), 2)

        def _assert_nationality(item, nationality, name):
            self.assertEqual(item['name'], name)
            self.assertIs(item['is_active'], nationality.is_active)
            self.assertIn('created_at', item)
            self.assertIn('updated_at', item)

        for item in items:
            pk = item['id']
            if pk == nation_ru.pk:
                _assert_nationality(item, nation_ru, 'Russian')
            if pk == nation_au.pk:
                _assert_nationality(item, nation_au, 'Australian')

    def test_create_nationality(self):

        payload = {
            'is_active': True,
            'country': self.countries['au'].id,
            'name': 'Australian'
        }

        response = self.post('/api/nationality/admin/create/', payload)

        # it is about the request responses success
        data = response.json()

        item = data.get('item')
        self.assertIsNot(item['id'], None)

    def test_toggle_active(self):

        nationality = self.create_nationality('ru', 'Орос', 'Russian', True)

        payload = {'is_active': True}
        self.post('/api/nationality/admin/{}/toggle-active/'.format(nationality.pk), payload)

        # идэвхитэй болгосон эсэх
        nationality_updated = Nationality.objects.get(pk=nationality.pk)
        self.assertTrue(nationality_updated.is_active, msg='Идэвхитэй болсон байх ёстой.')

    def test_delete_nationality(self):

        nationality = self.create_nationality('ru', 'Орос', 'Russian', True)

        self.post('/api/nationality/admin/{}/delete/'.format(nationality.pk))

        num_existing = Nationality.objects.filter(pk=nationality.pk).count()
        self.assertEqual(num_existing, 0)
