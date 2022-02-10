from pathlib import Path
import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponse
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase
from django.test import TransactionTestCase
from django.test import override_settings

from main.decorators import login_required
from main.decorators import admin_required
from main.decorators import json_decode_request_body

from country.models import Country, CountryLocale
from config.models import Config
from language.models import Language
from visa.person_number.views_admin import _generate_numbers as generate_visa_person_numbers
from visa.document.models import Document, DocumentField
from visa.visa.models import Visa, Person, ValueText, ValueDate, ValueChoice
from visa.kind.models import VisaKind, VisaKindDocument, VisaKindDiscount
from visa.field.models import Field, FieldText, FieldDate, FieldChoice


MEDIA_DIR_NAME = 'uploads_test'


def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


@override_settings(
    MEDIA_URL='/{}/'.format(MEDIA_DIR_NAME),
    MEDIA_ROOT=settings.BASE_DIR.parent / MEDIA_DIR_NAME,
)
class BaseTestCase(TransactionTestCase):

    @classmethod
    def tearDownClass(cls):
        media_path = settings.BASE_DIR.parent / MEDIA_DIR_NAME
        if media_path.exists():
            rm_tree(media_path)
        super().tearDownClass()

    def setup_users(self):
        User = get_user_model()
        self.superuser = User.objects.create_user(
            'superuser',
            'superuser@example.com.com',
            'superuser',
            is_superuser=True
        )
        self.usertamir = User.objects.create_user(
            'tamiraatsogbayar@gmail.com',
            'tamiraatsogbayar@gmail.com',
            'tamir',
            is_superuser=True
        )

    def create_country(self, *args, **kwargs):
        country = Country.objects.create(*args, **kwargs)
        return country

    def create_country_locale(self, lang_code_name, country, *args, **kwargs):
        locale = CountryLocale.objects.create(
            *args,
            language=self.languages[lang_code_name],
            country=country,
            **kwargs,
        )
        return locale

    def setup_languages(self):

        lang_mn = Language.objects.create(
            code_name='mn',
            name='Монгол хэл',
            name_local='Монгол хэл',
            is_active=True,
            is_default=False,
        )

        lang_ru = Language.objects.create(
            code_name='ru',
            name='Орос хэл',
            name_local='Русский',
            is_active=True,
            is_default=False,
        )

        lang_en = Language.objects.create(
            code_name='en',
            name='Англи хэл',
            name_local='English',
            is_active=True,
            is_default=True,
        )

        self.assertTrue(
            lang_en.is_default,
            '"{}" -ийн is_default=True байх ёстой.'.format(lang_en.code_name)
        )

        self.languages = {
            'mn': lang_mn,
            'en': lang_en,
            'ru': lang_ru,
            'default': lang_en,
        }

    def setup_countries(self):

        country_mn = self.create_country(is_active=True)
        self.create_country_locale('mn', country_mn, name='Монгол', nationality='Монгол')
        self.create_country_locale('en', country_mn, name='Mongolia', nationality='Mongolian')
        self.create_country_locale('ru', country_mn, name='Монголия', nationality='Монгольский')

        country_ru = self.create_country(is_active=True)
        self.create_country_locale('mn', country_ru, name='Орос', nationality='Орос')
        self.create_country_locale('en', country_ru, name='Russia', nationality='Russian')
        self.create_country_locale('ru', country_ru, name='Россия', nationality='Русский')

        country_au = self.create_country(is_active=True)
        self.create_country_locale('mn', country_au, name='Австрали', nationality='Австрали')
        self.create_country_locale('en', country_au, name='Australia', nationality='Australian')
        self.create_country_locale('ru', country_au, name='Австралия', nationality='Австралийский')

        self.countries = {
            'mn': country_mn,
            'au': country_au,
            'ru': country_ru,
        }

    def create_document_field(self, *args, **kwargs):
        doc_field = DocumentField.objects.create(*args, **kwargs)
        return doc_field

    def create_document(self, *args, **kwargs):
        document = Document.objects.create(*args, **kwargs)
        return document

    def create_field_text(self, field, *args, **kwargs):
        field_text = FieldText.objects.create(
            field=field,
            **kwargs
        )
        return field_text

    def create_field_date(self, field, *args, **kwargs):
        field_date = FieldDate.objects.create(
            field=field,
            **kwargs
        )
        return field_date

    def create_field_choice(self, field, *args, **kwargs):
        field_choice = FieldChoice.objects.create(
            field=field,
            **kwargs
        )
        return field_choice

    def create_field(self, *args, **kwargs):
        field = Field.objects.create(*args, **kwargs)
        return field

    def create_language(self, *args, **kwargs):
        lang = Language.objects.create(*args, **kwargs)
        return lang

    def create_visa_kind(self, *args, **kwargs):
        kind = VisaKind.objects.create(*args, **kwargs)
        return kind

    def create_visa(self, country_code_name, *args, **kwargs):
        visa = Visa.objects.create(
            *args,
            country=self.countries[country_code_name],
            **kwargs
        )
        return visa

    def create_person(self, *args, **kwargs):
        person = Person.objects.create(*args, **kwargs)
        return person

    def create_text_value(self, *args, **kwargs):
        value_text = ValueText.objects.create(*args, **kwargs)
        return value_text

    def create_date_value(self, *args, **kwargs):
        value_date = ValueDate.objects.create(*args, **kwargs)
        return value_date

    def create_choice_value(self, *args, **kwargs):
        value_choice = ValueChoice.objects.create(*args, **kwargs)
        return value_choice

    def create_visa_kind_discount(self, *args, **kwargs):
        discount = VisaKindDiscount.objects.create(*args, **kwargs)
        return discount

    def setup_visa_kind(self):
        kind_j = self.create_visa_kind(
            title='Touris J',
            description="If you want to travel to mongolia.",
            code_name='J',
            is_active=True,
            days_stay=30,
            days_valid=180,
            entry_kind=1,
            fee_person=40.00
        )
        kind_hg = self.create_visa_kind(
            title='Residense HG',
            description="If you want to stay in mongolia.",
            code_name='HG',
            is_active=True,
            days_stay=365,
            days_valid=180,
            entry_kind=1,
            fee_person=80.00
        )
        kind_s = self.create_visa_kind(
            title='Student S',
            description="If you want to study in mongolia.",
            is_active=False,
            days_stay=365,
            days_valid=180,
            entry_kind=1,
            fee_person=80.00
        )
        # document
        ordinary_passport = self.create_document(
            name='Ordinary Passport',
            is_active=True
        )
        diplomatic_passport = self.create_document(
            name='Diplomatic Passport',
            is_active=True
        )
        travel_document = self.create_document(
            name='Travel Document',
            is_active=False
        )

        VisaKindDocument.objects.create(
            visa_kind=kind_j,
            document=ordinary_passport
        )
        VisaKindDocument.objects.create(
            visa_kind=kind_j,
            document=diplomatic_passport
        )
        VisaKindDocument.objects.create(
            visa_kind=kind_j,
            document=travel_document
        )

        # Discounts
        self.create_visa_kind_discount(
            visa_kind=kind_j,
            num_person=5,
            percent=0.25
        )

        # Fields
        field_last_name = self.create_field(
            label="Last name",
            code_name="last_name",
            kind=1,
            description="some description here",
            is_required=True,
            is_required_error="Required!",
            is_fixed=True,
        )

        self.create_field_text(
            field=field_last_name,
            min_length=2,
            min_length_error="Your answer is too shoirt!",
            max_length=100,
            max_length_error="",
            regex_chars="[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-]+",
            regex_chars_error="no longer to approve special characters!"
        )

        field_first_name = self.create_field(
            label="First name",
            code_name="first_name",
            kind=1,
            description="some description here",
            is_required=True,
            is_required_error="Required!",
            is_fixed=True,
        )
        self.create_field_text(
            field=field_first_name,
            min_length=2,
            min_length_error="Your answer is too shoirt!",
            max_length=100,
            max_length_error="",
            regex_chars="[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-]+",
            regex_chars_error="no longer to approve special characters!"
        )

        field_gender = self.create_field(
            label="Gender",
            code_name="gender",
            kind=3,
            description="some description here",
            is_required=True,
            is_required_error="Required!",
            is_fixed=True,
        )
        gender_male = self.create_field_choice(
            field=field_gender,
            label="Male",
            code_name="male",
        )
        gender_female = self.create_field_choice(
            field=field_gender,
            label="Female",
            code_name="female",
        )

        field_birth_date = self.create_field(
            label="Birth Date",
            code_name="birth_date",
            kind=2,
            description="some description here",
            is_required=True,
            is_required_error="Required!",
            is_fixed=True,
        )
        self.create_field_date(
            field=field_birth_date,
            max_kind=2,
            max_now_delta=timedelta(days=180),
            max_date=None,
            max_date_error="Must be less then current date!",
            min_kind=1,
            min_now_delta=None,
            min_date=None,
            min_date_error=None,
        )
        field_dummy = self.create_field(
            label="dummy",
            code_name="dummy",
            kind=1,
            description="some description here",
            is_required=True,
            is_required_error="Required!",
            is_fixed=False,
        )
        self.create_field_text(
            field=field_dummy,
            min_length=2,
            min_length_error="Your answer is too shoirt!",
            max_length=100,
            max_length_error="",
            regex_chars="[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-]+",
            regex_chars_error="no longer to approve special characters!"
        )

        # DocumentField
        doc_field_first_name = self.create_document_field(
            document=ordinary_passport,
            field=field_first_name,
            sort_order=0
        )
        doc_field_last_name = self.create_document_field(
            document=ordinary_passport,
            field=field_last_name,
            sort_order=1
        )
        doc_field_gender = self.create_document_field(
            document=ordinary_passport,
            field=field_gender,
            sort_order=2
        )
        doc_field_birth_date = self.create_document_field(
            document=ordinary_passport,
            field=field_birth_date,
            sort_order=3
        )
        # DocumentField1
        doc_field_first_name1 = self.create_document_field(
            document=travel_document,
            field=field_first_name,
            sort_order=0
        )
        doc_field_last_name1 = self.create_document_field(
            document=travel_document,
            field=field_last_name,
            sort_order=1
        )
        doc_field_gender1 = self.create_document_field(
            document=travel_document,
            field=field_gender,
            sort_order=2
        )
        doc_field_birth_date1 = self.create_document_field(
            document=travel_document,
            field=field_birth_date,
            sort_order=3
        )
        # VisaRequest
        visa1 = self.create_visa(
            'au',
            visa_kind=kind_j,
            date_of_arrival='2021-05-01',
            days_stay=30,
            days_valid=180,
            entry_kind=VisaKind.ENTRY_KIND_SINGLE,
            fee_person=40.00,
            created_by=self.usertamir,
        )

        visa2 = self.create_visa(
            'au',
            visa_kind=kind_s,
            date_of_arrival='2021-05-01',
            days_stay=30,
            days_valid=180,
            entry_kind=VisaKind.ENTRY_KIND_SINGLE,
            fee_person=40.00,
            created_by=self.usertamir,
        )

        # Person
        person1 = self.create_person(
            visa=visa1,
            number=1,
            document=ordinary_passport,
            status=Person.STATUS_NEW,
        )
        person2 = self.create_person(
            visa=visa1,
            number=2,
            document=ordinary_passport,
            status=Person.STATUS_NEW,
        )

        self.people = {
            'person1': person1,
            'person2': person2,
        }

        self.visa_requests = {
            'visa1': visa1,
            'visa2': visa2
        }

        self.gender_choice = {
            'male': gender_male,
            'female': gender_female,
        }

        self.fields = {
            'first_name': field_first_name,
            'last_name': field_last_name,
            'gender': field_gender,
            'birth_date': field_birth_date,
            'dummy': field_dummy,
        }
        self.documents = {
            'ordinary_passport': ordinary_passport,
            'diplomatic_passport': diplomatic_passport,
            'travel_document': travel_document,
        }
        self.doc_fields = {
            'first_name': doc_field_first_name,
            'last_name': doc_field_last_name,
            'gender': doc_field_gender,
            'birth_date': doc_field_birth_date,
        }
        self.doc_fields1 = {
            'first_name': doc_field_first_name1,
            'last_name': doc_field_last_name1,
            'gender': doc_field_gender1,
            'birth_date': doc_field_birth_date1,
        }
        self.visa_kinds = {
            'j': kind_j,
            'hg': kind_hg,
            's': kind_s,
        }

    def setup_configs(self):
        values = [
            ('email_host', 'host_value'),
            ('email_port', 'port_value'),
            ('email_user', 'user_value'),
            ('email_password', 'user_password'),
            ('recaptcha_is_active', 'value_recaptcha_is_active'),
            ('recaptcha_site_key', 'value_recaptcha_site_key'),
            ('recaptcha_secret_key', 'value_recaptcha_secret_key'),
            ('recaptcha_verify_url', 'value_recaptcha_verify_url'),
        ]

        self.configs = {
            name: Config.objects.create(name=name, value=value)
            for name, value in values
        }

    def setup_visa_person_number(self):
        num_created = generate_visa_person_numbers(8, 40)
        self.assertEqual(num_created, 40, 'VisaPersonNumber-ийг үүсгэж чадсангүй!')

    def login_superuser(self):
        self.client.login(username='superuser', password='superuser')

    def setUp(self):
        self.setup_users()
        self.setup_languages()
        self.setup_countries()
        self.setup_visa_kind()
        self.setup_configs()
        self.setup_visa_person_number()

        self.client = Client()

    def post(self, *args, doAssert=True, **kwargs):

        response = self.client.post(
            *args,
            content_type='application/json',
            **kwargs,
        )

        if doAssert:
            data = response.json()

            # хариу зөв байх
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data.get('is_success'))

        return response

    def get(self, *args, doAssert=True, **kwargs):

        response = self.client.get(
            *args,
            content_type='application/json',
            **kwargs,
        )

        if doAssert:
            data = response.json()

            # хариу зөв байх
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data.get('is_success'))

        return response

    def assert_url_http200(self, url, payload, method='POST'):

        if method == 'POST':
            rsp = self.post(url, payload, doAssert=False)
        elif method == 'GET':
            rsp = self.get(url, doAssert=False)
        else:
            raise Exception('Undefined method {}'.format(method))

        self.assertEqual(rsp.status_code, 200)

        data = rsp.json()
        self.assertTrue(data.get('is_success'))

    def assert_url_http401(self, url, payload, method='GET'):

        if method == 'POST':
            rsp = self.post(url, payload, doAssert=False)
        elif method == 'GET':
            rsp = self.get(url, doAssert=False)
        else:
            raise Exception('Undefined method {}'.format(method))

        self.assertEqual(rsp.status_code, 401)

        data = rsp.json()
        self.assertFalse(data.get('is_success'))


class DecoratorTestCase(TestCase):

    def test_login_required_success(self):

        decorated_view = login_required(lambda v: 'view-executed')

        request = RequestFactory()
        request.user = type('User', (object,), {'is_authenticated': True})

        response = decorated_view(request)

        self.assertEqual(response, 'view-executed')

    def test_login_required_fail(self):

        decorated_view = login_required(lambda v: 'view-executed')

        request = RequestFactory()
        request.user = type('User', (object,), {'is_authenticated': False})

        response = decorated_view(request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        data = json.loads(response.content)
        self.assertFalse(data['is_success'])
        self.assertEqual(data['error'], 'login-required')

    def test_admin_required_success(self):

        decorated_view = login_required(lambda v: 'view-executed')

        request = RequestFactory()
        request.user = type('User', (object,), {
            'is_superuser': True,
            'is_authenticated': True,
        })

        response = decorated_view(request)

        self.assertEqual(response, 'view-executed')

    def test_admin_required_fail(self):

        decorated_view = admin_required(lambda v: 'view-executed')

        request = RequestFactory()
        request.user = type('User', (object,), {
            'is_superuser': False,
            'is_authenticated': True,
        })

        response = decorated_view(request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        data = json.loads(response.content)
        self.assertFalse(data['is_success'])
        self.assertEqual(data['error'], 'missing-permission')

    def test_json_decode_request_body_success(self):

        decorated_view = json_decode_request_body(lambda v: 'view-executed')

        request = RequestFactory()
        request.body = '{"value": 7}'

        response = decorated_view(request)

        self.assertEqual(response, 'view-executed')
        self.assertEqual(request.body_json_decoded['value'], 7)

    def test_json_decode_request_body_fail(self):

        decorated_view = json_decode_request_body(lambda v: 'view-executed')

        request = RequestFactory()
        request.body = 'not-a-json-content'

        response = decorated_view(request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        data = json.loads(response.content)
        self.assertFalse(data['is_success'])
