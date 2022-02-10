from main.tests import BaseTestCase
from visa.document.models import Document, DocumentField


class DocumentAdmin(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.login_superuser()

    def test_details(self):
        doc = self.documents['ordinary_passport']

        rsp = self.post(f'/api/visa/document/{doc.pk}/', {})
        item = rsp.json()['item']
        self.assertEqual(item['name'], doc.name)
        self.assertEqual(item['is_active'], doc.is_active)
        self.assertEqual(len(item['fields']), 7)

    def test_toggle_active(self):

        doc = self.documents['travel_document']
        payload = {
            'is_active': True
        }

        self.post(f'/api/visa/document/{doc.pk}/toggle-active/', payload)

        updated_doc = Document.objects.get(pk=doc.pk)
        self.assertTrue(updated_doc.is_active)

    def test_delete(self):
        document = self.documents['travel_document']

        self.post(f'/api/visa/document/{document.pk}/delete/', {})

        updated_doc = Document.objects.get(pk=document.pk)
        self.assertFalse(updated_doc.deleted_at is None)

    def test_delete_error(self):
        document = self.documents['ordinary_passport']

        rsp = self.post(f'/api/visa/document/{document.pk}/delete/', {}, doAssert=False)

        data = rsp.json()

        self.assertFalse(data['is_success'])
        self.assertEqual(data['error'], 'Идэвхтэй Бичиг баримтыг устгах боломжгүй!')

    def test_update(self):

        document = self.documents['travel_document']
        payload = {
            'name': 'new name',
            'doc_fields': []
        }

        rsp = self.post(f'/api/visa/document/{document.pk}/update/', payload)
        item = rsp.json()['item']
        updated_doc = Document.objects.get(pk=document.pk)
        doc_fields = DocumentField.objects.filter(document=updated_doc)

        self.assertEqual(item['name'], updated_doc.name)
        self.assertEqual(len(item['fields']), 7)
        self.assertEqual(doc_fields.count(), 4)

    def test_create(self):

        payload = {
            'name': 'certification of born',
            'doc_fields': [

            ]
        }

        rsp = self.post('/api/visa/document/create/', payload, doAssert=False)
        item = rsp.json()['item']

        self.assertEqual(item['name'], 'certification of born')
        self.assertEqual(len(item['fields']), 7)

        self.assertEqual(item['fields'][0]['code_name'], self.fields['last_name'].code_name)
        self.assertEqual(item['fields'][1]['code_name'], self.fields['first_name'].code_name)
        self.assertEqual(item['fields'][2]['code_name'], self.fields['gender'].code_name)

    def test_list(self):

        rsp = self.post('/api/visa/document/all/', {})

        items = rsp.json()['items']
        items_map = {item['id']: item for item in items}

        def _assert_document(item, document):
            self.assertEqual(item['name'], document.name)
            self.assertEqual(item['is_active'], document.is_active)

        self.assertEqual(len(items), 3)
        self.assertIn(self.documents['ordinary_passport'].pk, items_map)
        self.assertIn(self.documents['diplomatic_passport'].pk, items_map)
        self.assertIn(self.documents['travel_document'].pk, items_map)

        for document in self.documents.values():
            _assert_document(items_map[document.id], document)
