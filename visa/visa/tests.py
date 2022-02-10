from django.core import mail

from main.tests import BaseTestCase
from io import BytesIO
import base64
from PIL import Image
from .models import Visa, Person, ValueText, ValueDate, ValueChoice


class VisaAdmin(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.login_superuser()

    def test_visa_decline(self):

        person = self.people['person1']
        payload = {
            'language': self.languages['en'].code_name
        }

        rsp = self.post(f'/api/visa/admin/{person.pk}/decline/', payload, doAssert=False)

        item = rsp.json()['item']

        email = mail.outbox[0]

        self.assertEqual(len(email.to), 1)
        self.assertEqual(email.to[0], person.visa.created_by.email)

        self.assertEqual(item['status'], Person.STATUS_DECLINE)
        self.assertEqual(item['updated_by'], self.superuser.username)

    def test_visa_approve(self):

        person = self.people['person1']
        payload = {
            'language': self.languages['en'].code_name
        }
        rsp = self.post(f'/api/visa/admin/{person.pk}/approve/', payload, doAssert=False)
        item = rsp.json()['item']

        email = mail.outbox[0]

        self.assertEqual(len(email.to), 1)
        self.assertEqual(email.to[0], person.visa.created_by.email)
        self.assertTrue(email.attachments)
        self.assertEqual(item['status'], Person.STATUS_APPROVE)
        self.assertEqual(item['updated_by'], self.superuser.username)

    def test_details(self):

        person = self.people['person1']

        rsp = self.post(f'/api/visa/admin/{person.pk}/', {})

        item = rsp.json()['item']
        self.assertEqual(item['id'], person.id)
        self.assertEqual(item['visa_kind'], person.visa.visa_kind.title)
        self.assertEqual(item['country'], person.visa.country.get_default_name())
        self.assertEqual(item['status'], person.status)

    def test_visa_list(self):

        payload = {
            'page': 1,
            'search': True,
            'text': '',
            'kind': self.visa_kinds['j'].pk,
            'start_date': '',
            'end_date': '',
            'status': Person.STATUS_NEW,
            'sort_direction': 'desc',
            'sort_key': 'number',
        }

        rsp = self.post('/api/visa/admin/list/', payload, doAssert=False)

        results = rsp.json()['results']
        self.assertEqual(len(results), 2)


class VisaPublic(BaseTestCase):

    def _create_image(self):

        buffered = BytesIO()
        image = Image.new('RGB', (350, 350), color='red')
        image.save(buffered, format="PNG")

        img = base64.b64encode(buffered.getvalue()).decode()

        return img

    def setUp(self):
        super().setUp()
        self.login_superuser()

        self.image = self._create_image()

    def test_visa_submit(self):

        first_name = self.doc_fields['first_name']
        last_name = self.doc_fields['last_name']
        gender = self.doc_fields['gender']
        birth_date = self.doc_fields['birth_date']

        payload = {
            'visa_kind': self.visa_kinds['j'].pk,
            'country': self.countries['au'].pk,
            'date_of_arrival': '2021-05-01',
            'email': 'tamiraagbayar@gmail.com',
            'phone': '883773471',
            'address': 'USA Applewood 1600 19',
            'person': [
                {
                    'image_portrait': self.image,
                    'image_document': self.image,
                    'document': self.documents['ordinary_passport'].pk,
                    'values': [
                        {
                            'doc_field': first_name.pk,
                            'field': first_name.field.pk,
                            'value': 'Tamir',
                        },
                        {
                            'doc_field': last_name.pk,
                            'field': last_name.field.pk,
                            'value': 'Tsogbayr',
                        },
                        {
                            'doc_field': gender.pk,
                            'field': gender.field.pk,
                            'value': self.gender_choice['male'].pk,
                        },
                        {
                            'doc_field': birth_date.pk,
                            'field': birth_date.field.pk,
                            'value': '1995-10-22',
                        },
                    ]
                },
                {
                    'image_portrait': self.image,
                    'image_document': self.image,
                    'document': self.documents['ordinary_passport'].pk,
                    'values': [
                        {
                            'doc_field': first_name.pk,
                            'field': first_name.field.pk,
                            'value': 'Zolboo',
                        },
                        {
                            'doc_field': last_name.pk,
                            'field': last_name.field.pk,
                            'value': 'Tsogbayr',
                        },
                        {
                            'id': gender.pk,
                            'doc_field': gender.pk,
                            'field': gender.field.pk,
                            'value': self.gender_choice['male'].pk,
                        },
                        {
                            'doc_field': birth_date.pk,
                            'field': birth_date.field.pk,
                            'value': '1997-04-22',
                        },
                    ]
                }
            ],
        }
        rsp = self.post('/api/visa/submit/', payload, doAssert=False)

        item = rsp.json()['item']

        visa = Visa.objects.get(pk=item['id'])
        people = Person.objects.filter(visa=visa)

        self.assertEqual(len(item['person']), 2)
        self.assertEqual(visa.visa_kind, self.visa_kinds['j'])
        self.assertEqual(visa.country, self.countries['au'])
        self.assertEqual(visa.date_of_arrival.strftime("%Y-%m-%d"), '2021-05-01')

        (person1, person2) = people

        # Person 1

        value_first_name = ValueText.objects.get(person=person1, document_field=first_name)
        value_last_name = ValueText.objects.get(person=person1, document_field=last_name)
        value_birth_date = ValueDate.objects.get(person=person1, document_field=birth_date)
        value_gender = ValueChoice.objects.get(person=person1, document_field=gender)
        self.assertEqual(value_first_name.value, 'Tamir')
        self.assertEqual(value_last_name.value, 'Tsogbayr')
        self.assertEqual(value_birth_date.value.strftime("%Y-%m-%d"), '1995-10-22')
        self.assertEqual(value_gender.value.code_name, 'male')

        # Person 2

        value_first_name = ValueText.objects.get(person=person2, document_field=first_name)
        value_last_name = ValueText.objects.get(person=person2, document_field=last_name)
        value_birth_date = ValueDate.objects.get(person=person2, document_field=birth_date)
        value_gender = ValueChoice.objects.get(person=person2, document_field=gender)
        self.assertEqual(value_first_name.value, 'Zolboo')
        self.assertEqual(value_last_name.value, 'Tsogbayr')
        self.assertEqual(value_birth_date.value.strftime("%Y-%m-%d"), '1997-04-22')
        self.assertEqual(value_gender.value.code_name, 'male')
