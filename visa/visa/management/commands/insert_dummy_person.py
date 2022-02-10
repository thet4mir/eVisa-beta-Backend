from django.core.management.base import BaseCommand
from django.apps import apps
from visa.visa.models import Visa, Person, ValueText, ValueDate, ValueChoice
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from visa.document.models import Document, DocumentField
from visa.field.models import Field, FieldChoice


class Command(BaseCommand):

    help = """
        Insert Dummy person data in the database for list
    """

    def handle(self, *args, **options):

        doc = Document.objects.get(pk=53)
        doc_fields = DocumentField.objects.filter(document=doc)
        choice_doc_field = DocumentField.objects.get(document=doc, field__code_name='sex')

        male = FieldChoice.objects.get(field=choice_doc_field.field, code_name='male')
        female = FieldChoice.objects.get(field=choice_doc_field.field, code_name='female')

        data = [
            {
                "id": 1,
                "name": "Leanne",
                "surname": "Graham",
                "dateofbirth": "1990-05-20",
                "sex": male,
                "dateofexpiry": "2021-11-30",
            },
            {
                "id": 2,
                "name": "Ervin",
                "surname": "Howell",
                "dateofbirth": "1999-04-20",
                "sex": female,
                "dateofexpiry": "2021-09-30",
            },
            {
                "id": 3,
                "name": "Clementine",
                "surname": "Bauch",
                "dateofbirth": "1989-01-20",
                "sex": female,
                "dateofexpiry": "2021-12-30",
            },
            {
                "id": 4,
                "name": "Patricia ",
                "surname": "Lebsack",
                "dateofbirth": "1990-04-20",
                "sex": male,
                "dateofexpiry": "2022-01-30",
            },
            {
                "id": 5,
                "name": "Chelsey",
                "surname": "Dietrich",
                "dateofbirth": "1995-04-20",
                "sex": female,
                "dateofexpiry": "2022-11-30",
            },
            {
                "id": 6,
                "name": "Dennis ",
                "surname": "Schulist",
                "dateofbirth": "1988-04-20",
                "sex": male,
                "dateofexpiry": "2021-12-30",
            },
            {
                "id": 7,
                "name": "Kurtis",
                "surname": "Weissnat",
                "dateofbirth": "1991-04-20",
                "sex": male,
                "dateofexpiry": "2021-10-30",
            },
            {
                "id": 8,
                "name": "Nicholas",
                "surname": "Runolfsdottir",
                "dateofbirth": "1997-04-22",
                "sex": female,
                "dateofexpiry": "2022-02-10",
            },
            {
                "id": 9,
                "name": "Glenna",
                "surname": "Reichert",
                "dateofbirth": "1978-04-20",
                "sex": female,
                "dateofexpiry": "2021-10-30",
            },
            {
                "id": 10,
                "name": "Clementina",
                "surname": "DuBuque",
                "dateofbirth": "1996-05-14",
                "sex": male,
                "dateofexpiry": "2022-10-22",
            }
        ]
        rsp = input('Are you sure to insert person data to person model ? (Y/n): ')

        if rsp.lower() != 'y':
            print('\n Aborting...\n')
            return

        Country = apps.get_model('country', 'Country')
        VisaKind = apps.get_model('visa_kind', 'VisaKind')
        VisaPersonNumber = apps.get_model('visa_person_number', 'VisaPersonNumber')

        User = get_user_model()

        visa = Visa()
        visa.visa_kind = VisaKind.objects.all().first()
        visa.country = Country.objects.all().first()
        visa.date_of_arrival = timezone.now()
        visa.days_stay = 30
        visa.days_valid = 180
        visa.entry_kind = VisaKind.ENTRY_KIND_SINGLE
        visa.fee_person = 40.00
        visa.created_by = User.objects.all().first()
        visa.save()

        for idx, person in enumerate(range(10)):
            number = VisaPersonNumber.objects.filter(is_used=False).first()
            person = Person()
            person.visa = visa
            person.number = number.id
            person.document = doc
            person.image_document = SimpleUploadedFile('document.jpeg', '', content_type='iamge/jpeg')
            person.image_portrait = SimpleUploadedFile('portrait.jpeg', '', content_type='iamge/jpeg')
            person.save()

            number.is_used = True
            number.save()

            for doc_field in doc_fields:
                if doc_field.field.kind == Field.KIND_TEXT:
                    ValueText.objects.create(
                        person=person,
                        document_field=doc_field,
                        value=data[idx][doc_field.field.code_name]
                    )
                elif doc_field.field.kind == Field.KIND_DATE:
                    ValueDate.objects.create(
                        person=person,
                        document_field=doc_field,
                        value=data[idx][doc_field.field.code_name]
                    )
                elif doc_field.field.kind == Field.KIND_CHOICES:
                    ValueChoice.objects.create(
                        person=person,
                        document_field=doc_field,
                        value=data[idx][doc_field.field.code_name]
                    )

        people = Person.objects.all().count()

        self.stdout.write(self.style.SUCCESS('Successfully %s rows inserted in person model' % people))
