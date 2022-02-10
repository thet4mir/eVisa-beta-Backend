from main.tests import BaseTestCase
from visa.field.models import Field, FieldText, FieldDate, FieldChoice


class FieldAdmin(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.login_superuser()

    def test_create_choice_error(self):

        payload = {
            'label': 'first name',
            'code_name': 'first_name',
            'kind': 3,
            'description': 'some information about this field.',
            'is_required': 1,
            'is_required_error': 'You must fill this field!',
        }

        rsp = self.post('/api/visa/field/create/', payload, doAssert=False)

        form_errors = rsp.json()['form_errors']

        self.assertEqual(form_errors['options'], 'Та сонголтуудыг оруулна уу!')

    def test_create_errors(self):

        payload = {
            'label': 'first name',
            'code_name': 'first_name',
            'kind': 3,
            'description': 'some information about this field.',
            'is_required': True,
            'is_required_error': 'You must fill this field!',
            'options': [
                {
                    "label": "",
                    "code_name": "male1",
                },
                {
                    "label": "Эмэгтэй",
                    "code_name": "",
                },
            ],
        }

        rsp = self.post('/api/visa/field/create/', payload, doAssert=False)
        errors = rsp.json()['form_errors']

        self.assertIn('options', errors)

    def test_delete_fixed_field(self):

        field = self.fields['first_name']

        rsp = self.post(f'/api/visa/field/{field.pk}/delete/', {}, doAssert=False)

        errors = rsp.json()['errors']
        self.assertEqual(errors , 'Fixed field-ийг устгах боломжгүй!')

    def test_delete(self):

        field = self.fields['dummy']

        self.post(f'/api/visa/field/{field.pk}/delete/', {}, doAssert=False)

        updated_field = Field.objects.get(pk=field.pk)
        self.assertFalse(updated_field.deleted_at is None)

    def test_date_details(self):

        field = self.fields['birth_date']

        rsp = self.post(f'/api/visa/field/{field.pk}/', {})

        item = rsp.json()['item']
        updated_field = Field.objects.get(pk=field.pk)
        field_date = FieldDate.objects.get(field=updated_field)

        self.assertEqual(updated_field.label, item['label'])
        self.assertEqual(updated_field.code_name, item['code_name'])
        self.assertEqual(updated_field.kind, item['kind'])
        self.assertEqual(updated_field.description, item['description'])
        max_delta = field_date.max_now_delta.total_seconds() if field_date.max_now_delta else None
        min_delta = field_date.min_now_delta.total_seconds() if field_date.min_now_delta else None
        self.assertEqual(item['max_now_delta'], max_delta)
        self.assertEqual(item['min_now_delta'], min_delta)

    def test_details(self):

        field = self.fields['first_name']

        rsp = self.post(f'/api/visa/field/{field.pk}/', {})

        item = rsp.json()['item']
        updated_field = Field.objects.get(pk=field.pk)
        field_text = FieldText.objects.get(field=updated_field)

        self.assertEqual(updated_field.label, item['label'])
        self.assertEqual(updated_field.code_name, item['code_name'])
        self.assertEqual(updated_field.kind, item['kind'])
        self.assertEqual(updated_field.description, item['description'])
        self.assertEqual(field_text.min_length, item['min_length'])
        self.assertEqual(field_text.min_length_error, item['min_length_error'])
        self.assertEqual(field_text.max_length, item['max_length'])
        self.assertEqual(field_text.max_length_error, item['max_length_error'])
        self.assertEqual(field_text.regex_chars, item['regex_chars'])
        self.assertEqual(field_text.regex_chars_error, item['regex_chars_error'])

    def test_create_choice_field(self):

        payload = {
            'label': 'first name',
            'code_name': 'first_name',
            'kind': 3,
            'description': 'some information about this field.',
            'is_required': True,
            'is_required_error': 'You must fill this field!',
            'options': [
                {
                    "label": "Эрэгтэй",
                    "code_name": "male1",
                },
                {
                    "label": "Эмэгтэй",
                    "code_name": "female1",
                },
            ],
        }

        rsp = self.post('/api/visa/field/create/', payload, doAssert=False)
        item = rsp.json()['item']

        self.assertEqual(item['label'], 'first name')
        self.assertEqual(item['code_name'], 'first_name')
        self.assertEqual(item['kind'], 3)
        self.assertEqual(item['description'], 'some information about this field.')
        self.assertEqual(item['is_required'], True)
        self.assertEqual(item['is_required_error'], 'You must fill this field!')
        self.assertEqual(len(item['options']), 2)
        self.assertEqual(item['options'][0]['label'], 'Эрэгтэй')
        self.assertEqual(item['options'][0]['code_name'], 'male1')
        self.assertEqual(item['options'][1]['label'], 'Эмэгтэй')
        self.assertEqual(item['options'][1]['code_name'], 'female1')

    def test_update_choice_field(self):

        field = self.fields['gender']

        payload = {
            'label': 'new label',
            'code_name': 'gender',
            'kind': 3,
            'description': 'new description.',
            'is_required': True,
            'is_required_error': '',
            'options': [
                {
                    'id': self.gender_choice['male'].pk,
                    "label": "new label",
                    "code_name": "male",
                },
                {
                    'id': self.gender_choice['female'].pk,
                    "label": "Female",
                    "code_name": "female",
                },
                {
                    "label": "other",
                    "code_name": "other",
                },
            ],
        }

        rsp = self.post(f'/api/visa/field/{field.id}/update/', payload, doAssert=False)
        item = rsp.json()['item']

        updated_field = Field.objects.get(pk=field.pk)
        options = FieldChoice.objects.filter(field=updated_field, is_deleted=False)

        self.assertEqual(updated_field.label, item['label'])
        self.assertEqual(updated_field.code_name, item['code_name'])
        self.assertEqual(updated_field.kind, item['kind'])
        self.assertEqual(updated_field.description, item['description'])
        self.assertEqual(updated_field.is_required, item['is_required'])
        self.assertEqual(updated_field.is_required_error, item['is_required_error'])
        self.assertEqual(options.count(), 3)
        self.assertEqual(options[0].label, item['options'][0]['label'])
        self.assertEqual(options[0].code_name, item['options'][0]['code_name'])
        self.assertEqual(options[1].label, item['options'][1]['label'])
        self.assertEqual(options[1].code_name, item['options'][1]['code_name'])
        self.assertEqual(options[2].label, item['options'][2]['label'])
        self.assertEqual(options[2].code_name, item['options'][2]['code_name'])

    def test_create_date_field(self):

        payload = {
            'label': 'first name',
            'code_name': 'first_name',
            'kind': 2,
            'description': 'some information about this field.',
            'is_required': True,
            'is_required_error': 'You must fill this field!',
            'max_kind': 2,
            'max_now_delta': 86400,
            'max_date': '',
            'max_date_error': "Must be less then current date!",
            'min_kind': 1,
            'min_now_delta': 86400,
            'min_date': '',
            'min_date_error': '',
        }

        rsp = self.post('/api/visa/field/create/', payload, doAssert=False)
        item = rsp.json()['item']
        self.assertEqual(item['label'], 'first name')
        self.assertEqual(item['code_name'], 'first_name')
        self.assertEqual(item['kind'], 2)
        self.assertEqual(item['description'], 'some information about this field.')
        self.assertEqual(item['is_required'], True)
        self.assertEqual(item['is_required_error'], 'You must fill this field!')
        self.assertEqual(item['max_kind'], 2)
        self.assertEqual(item['max_now_delta'], 86400)
        self.assertEqual(item['max_date'], None)
        self.assertEqual(item['max_date_error'], 'Must be less then current date!')
        self.assertEqual(item['min_kind'], 1)
        self.assertEqual(item['min_now_delta'], 86400)
        self.assertEqual(item['min_date'], None)
        self.assertEqual(item['min_date_error'], None)

    def test_update_date_field(self):

        field = self.fields['birth_date']

        payload = {
            'label': 'new lable',
            'code_name': 'birth_date',
            'kind': 2,
            'description': 'new description.',
            'is_required': True,
            'is_required_error': '',
            'max_kind': 2,
            'max_now_delta': '',
            'max_date': '',
            'max_date_error': "new max message",
            'min_kind': 1,
            'min_now_delta': '',
            'min_date': '',
            'min_date_error': 'new min message',
        }

        rsp = self.post(f'/api/visa/field/{field.pk}/update/', payload)

        item = rsp.json()['item']
        updated_field = Field.objects.get(pk=field.pk)
        field_date = FieldDate.objects.get(field=updated_field)

        self.assertEqual(updated_field.label, item['label'])
        self.assertEqual(updated_field.code_name, item['code_name'])
        self.assertEqual(updated_field.kind, item['kind'])
        self.assertEqual(updated_field.description, item['description'])
        self.assertEqual(updated_field.is_required, item['is_required'])
        self.assertEqual(updated_field.is_required_error, item['is_required_error'])
        self.assertEqual(field_date.max_kind, item['max_kind'])
        self.assertEqual(field_date.max_now_delta, item['max_now_delta'])
        self.assertEqual(field_date.max_date, item['max_date'])
        self.assertEqual(field_date.max_date_error, item['max_date_error'])
        self.assertEqual(field_date.min_kind, item['min_kind'])
        self.assertEqual(field_date.min_now_delta, item['min_now_delta'])
        self.assertEqual(field_date.min_date, item['min_date'])
        self.assertEqual(field_date.min_date_error, item['min_date_error'])

    def test_create_text_field(self):

        payload = {
            'label': 'first name',
            'code_name': 'first_name',
            'kind': 1,
            'description': 'some information about this field.',
            'is_required': 1,
            'is_required_error': 'You must fill this field!',
            'min_length': '',
            'min_length_error': '',
            'max_length': 100,
            'max_length_error': '',
            'regex_chars': "[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-]+",
            'regex_chars_error': "no longer to approve special characters!"
        }

        rsp = self.post('/api/visa/field/create/', payload)

        item = rsp.json()['item']

        self.assertEqual(item['label'], 'first name')
        self.assertEqual(item['code_name'], 'first_name')
        self.assertEqual(item['kind'], 1)
        self.assertEqual(item['description'], 'some information about this field.')
        self.assertEqual(item['is_required'], True)
        self.assertEqual(item['is_required_error'], 'You must fill this field!')
        self.assertEqual(item['min_length'], None)
        self.assertEqual(item['min_length_error'], None)
        self.assertEqual(item['max_length'], 100)
        self.assertEqual(item['max_length_error'], None)
        self.assertEqual(item['regex_chars'], "[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-]+")
        self.assertEqual(item['regex_chars_error'], "no longer to approve special characters!")

    def test_update_text_field(self):

        field = self.fields['first_name']
        payload = {
            'label': 'new lable',
            'code_name': 'first_name',
            'kind': 1,
            'description': 'new description.',
            'is_required': True,
            'is_required_error': '',
            'min_length': 10,
            'min_length_error': 'new min length error',
            'max_length': 100,
            'max_length_error': "new max length error",
            'regex_chars': "new regex chars",
            'regex_chars_error': "new regex chars length error"
        }

        rsp = self.post(f'/api/visa/field/{field.pk}/update/', payload, doAssert=False)

        item = rsp.json()['item']
        updated_field = Field.objects.get(pk=field.pk)
        field_text = FieldText.objects.get(field=updated_field)

        self.assertEqual(updated_field.label, item['label'])
        self.assertEqual(updated_field.code_name, item['code_name'])
        self.assertEqual(updated_field.kind, item['kind'])
        self.assertEqual(updated_field.description, item['description'])
        self.assertEqual(updated_field.is_required, item['is_required'])
        self.assertEqual(updated_field.is_required_error, item['is_required_error'])
        self.assertEqual(field_text.min_length, item['min_length'])
        self.assertEqual(field_text.min_length_error, item['min_length_error'])
        self.assertEqual(field_text.max_length, item['max_length'])
        self.assertEqual(field_text.max_length_error, item['max_length_error'])
        self.assertEqual(field_text.regex_chars, item['regex_chars'])
        self.assertEqual(field_text.regex_chars_error, item['regex_chars_error'])

    def test_list(self):

        rsp = self.post('/api/visa/field/all/', {})

        items = rsp.json()['items']
        items_map = {item['id']: item for item in items}

        def _assert_field(item, field):
            self.assertEqual(item['label'], field.label)
            self.assertEqual(item['code_name'], field.code_name)
            self.assertEqual(item['kind'], field.kind)

        self.assertEqual(len(items), 5)

        for field in self.fields.values():
            _assert_field(items_map[field.id], field)
