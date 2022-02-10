from main.tests import BaseTestCase
from django.shortcuts import get_object_or_404
from .models import VisaKind


class VisaKindAdmin(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.login_superuser()

    def test_days_stay_error(self):

        payload = {
            'title': 'Visa Kind A',
            'description': "If you want to bambirdaltsah in mongolia.",
            'code_name': 'A',
            'is_active': True,
            'days_stay': 280,
            'days_valid': 180,
            'entry_kind': 1,
            'fee_person': 80.00,
            'documents': [
                self.documents['diplomatic_passport'].pk,
                self.documents['travel_document'].pk,
            ],
            'visa_exempt_country': [
                self.countries['mn'].pk,
                self.countries['au'].pk,
                self.countries['ru'].pk,
            ],
            'fee_exempt_country': [
                self.countries['mn'].pk,
                self.countries['au'].pk,
                self.countries['ru'].pk,
            ],
            'discount_list': [
                {
                    'num_person': 10,
                    'percent': 0.5,
                },
                {
                    'num_person': 15,
                    'percent': 0.75,
                },
            ]
        }

        rsp = self.post('/api/visa/kind/create/', payload, doAssert=False)

        form_errors = rsp.json()['form_errors']

        self.assertEqual(form_errors['days_stay'][0], 'Хүчинтэй хугацаанаас хэтэрсэн байна')

    def test_delete_error(self):

        kind = self.visa_kinds['j']

        rsp = self.post(f'/api/visa/kind/{kind.pk}/delete/', {}, doAssert=False)

        data = rsp.json()['errors']

        self.assertEqual(data, "Идэвхтэй төрлийг устгах боломгүй!")

    def test_delete(self):

        kind = self.visa_kinds['s']

        self.post(f'/api/visa/kind/{kind.pk}/delete/', {})

        updated_kind = get_object_or_404(VisaKind, pk=kind.pk)

        self.assertFalse(updated_kind.deleted_at is None)

    def test_toggle_active(self):

        kind = self.visa_kinds['j']
        payload = {
            'is_active': False,
        }

        self.post(f'/api/visa/kind/{kind.pk}/toggle-active/', payload)

        updated_kind = get_object_or_404(VisaKind, pk=kind.pk)

        self.assertFalse(updated_kind.is_active)

    def test_update(self):

        kind = self.visa_kinds['j']
        payload = {
            'title': 'title updated',
            'description': "description updated",
            'code_name': 'B',
            'is_active': False,
            'days_stay': 30,
            'days_valid': 180,
            'entry_kind': 1,
            'fee_person': 1.00,
            'documents': [
                self.documents['travel_document'].pk,
            ],
            'visa_exempt_country': [
                self.countries['mn'].pk,
                self.countries['au'].pk,
                self.countries['ru'].pk,
            ],
            'fee_exempt_country': [
                self.countries['mn'].pk,
                self.countries['au'].pk,
                self.countries['ru'].pk,
            ],
            'discount_list': [
                {
                    'num_person': 5,
                    'percent': 0.25,
                },
                {
                    'num_person': 10,
                    'percent': 0.5,
                },
                {
                    'num_person': 15,
                    'percent': 75,
                },
            ]
        }

        rsp = self.post(f'/api/visa/kind/{kind.pk}/update/', payload, doAssert=False)

        item = rsp.json()['item']

        self.assertEqual(item['title'], 'title updated')
        self.assertEqual(item['description'], 'description updated')
        self.assertEqual(item['code_name'], 'B')
        self.assertFalse(item['is_active'])
        self.assertEqual(item['days_stay'], 30)
        self.assertEqual(item['entry_kind'], 1)
        self.assertEqual(float(item['fee_person']), 1.00)
        self.assertEqual(len(item['documents']), 1)
        self.assertEqual(len(item['discount_list']), 3)

    def test_create(self):

        payload = {
            'title': 'Visa Kind A',
            'description': "If you want to bambirdaltsah in mongolia.",
            'code_name': 'A',
            'is_active': True,
            'days_stay': 30,
            'days_valid': 180,
            'entry_kind': 1,
            'fee_person': 80.79,
            'documents': [
                self.documents['diplomatic_passport'].pk,
                self.documents['travel_document'].pk,
            ],
            'visa_exempt_country': [
                self.countries['mn'].pk,
                self.countries['au'].pk,
                self.countries['ru'].pk,
            ],
            'fee_exempt_country': [
                self.countries['mn'].pk,
                self.countries['au'].pk,
                self.countries['ru'].pk,
            ],
            'discount_list': [
                {
                    'num_person': 10,
                    'percent': 0.5,
                },
                {
                    'num_person': 15,
                    'percent': 0.75,
                },
            ]
        }

        rsp = self.post('/api/visa/kind/create/', payload, doAssert=False)
        item = rsp.json()['item']

        self.assertEqual(item['title'], 'Visa Kind A')
        self.assertEqual(item['description'], "If you want to bambirdaltsah in mongolia.")
        self.assertEqual(item['code_name'], "A")
        self.assertTrue(item['is_active'])
        self.assertEqual(item['days_stay'], 30)
        self.assertEqual(item['days_valid'], 180)
        self.assertEqual(item['entry_kind'], 1)
        self.assertEqual(float(item['fee_person']), 80.79)
        self.assertEqual(len(item['documents']), 2)
        self.assertEqual(len(item['discount_list']), 2)

    def test_list(self):

        rsp = self.post('/api/visa/kind/all/', {}, doAssert=False)
        items = rsp.json()['items']
        items_map = {item['id']: item for item in items}

        def _assert_visa_kind(item, kind):
            self.assertEqual(item['title'], kind.title)
            self.assertEqual(item['description'], kind.description)
            self.assertEqual(item['code_name'], kind.code_name)
            self.assertEqual(item['is_active'], kind.is_active)
            self.assertEqual(item['days_stay'], kind.days_stay)
            self.assertEqual(item['days_valid'], kind.days_valid)
            self.assertEqual(item['entry_kind'], kind.entry_kind)
            self.assertEqual(float(item['fee_person']), kind.fee_person)

        for kind in self.visa_kinds.values():
            _assert_visa_kind(items_map[kind.id], kind)


class VisaKindPublic(BaseTestCase):

    def test_public_list(self):

        rsp = self.post('/api/visa/kind/public/all/', {}, doAssert=False)

        items = rsp.json()['items']

        self.assertEqual(len(items), 2)
        self.assertIn('id', items[0])
        self.assertIn('title', items[0])
        self.assertIn('description', items[0])
        self.assertIn('code_name', items[0])
        self.assertIn('days_stay', items[0])
        self.assertIn('days_valid', items[0])
        self.assertIn('entry_kind', items[0])
        self.assertIn('fee_person', items[0])

        self.assertIn('id', items[1])
        self.assertIn('title', items[1])
        self.assertIn('description', items[1])
        self.assertIn('days_stay', items[1])
        self.assertIn('days_valid', items[1])
        self.assertIn('entry_kind', items[1])
        self.assertIn('fee_person', items[1])

    def test_public_details(self):

        kind = self.visa_kinds['j']

        rsp = self.post(f'/api/visa/kind/public/{kind.pk}/', {}, doAssert=False)

        item = rsp.json()['item']

        self.assertEqual(item['title'], kind.title)
        self.assertEqual(item['description'], kind.description)
        self.assertEqual(item['code_name'], kind.code_name)
        self.assertEqual(item['days_stay'], kind.days_stay)
        self.assertEqual(item['days_valid'], kind.days_valid)
        self.assertEqual(item['entry_kind'], kind.entry_kind)
        self.assertEqual(item['fee_person'], kind.fee_person)
        self.assertEqual(len(item['documents']), 2)
        self.assertEqual(len(item['documents'][0]['fields']), 6)
        self.assertIn('visa_exempt_country', item)
        self.assertEqual(len(item['visa_exempt_country']), 0)
        self.assertIn('fee_exempt_country', item)
        self.assertEqual(len(item['fee_exempt_country']), 0)
        self.assertIn('discount_list', item)
        self.assertEqual(len(item['discount_list']), 1)
