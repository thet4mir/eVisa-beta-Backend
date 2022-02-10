from datetime import timedelta
from django.db import migrations
from visa.field.models import Field, FieldChoice, FieldDate, FieldText


def fixed_fields(apps, schema_editor):

    items = [
        {
            'field':{
                'label': 'First Name',
                'code_name': 'name',
                'kind': 1,
                'description': '',
                'is_fixed': True,
                'is_required': True,
                'is_required_error': 'This field is required!',
            },
            'sub_field':{
                'min_length': 2,
                'min_length_error': 'Ensure this value at least [limit] characters!',
                'max_length': 100,
                'max_length_error': 'Ensure this value at most [limit] characters!',
                'regex_chars': '[a-zA-Z,-0-9]+',
                'regex_chars_error': 'Enter a valid value!',
            }
        },
        {
            'field':{
                'label': 'Last Name',
                'code_name': 'surname',
                'kind': 1,
                'description': '',
                'is_fixed': True,
                'is_required': True,
                'is_required_error': 'This field is required!',
            },
            'sub_field': {
                'min_length': 2,
                'min_length_error': 'Ensure this value at least [limit] characters!',
                'max_length': 100,
                'max_length_error': 'Ensure this value at most [limit] characters!',
                'regex_chars': '[a-zA-Z,-0-9]+',
                'regex_chars_error': 'Enter a valid value!',
            }
        },
        {
            'field':{
                'label': 'Birth Day',
                'code_name': 'dateofbirth',
                'kind': 2,
                'description': '',
                'is_fixed': True,
                'is_required': True,
                'is_required_error': 'This field is required!',
            },
            'sub_field': {
                'max_kind': 2,
                'max_now_delta': timedelta(days=0),
                'max_date': None,
                'max_date_error': 'Maximum allowed date is [limit]',
                'min_kind': 1,
                'min_now_delta': None,
                'min_date': None,
                'min_date_error': ''
            }
        },
        {
            'field':{
                'label': 'Gender',
                'code_name': 'sex',
                'kind': 3,
                'description': '',
                'is_fixed': True,
                'is_required': True,
                'is_required_error': 'This field is required!',
            },
            'options': [
                {
                    'label': 'Male',
                    'code_name': 'male'
                },
                {
                    'label': 'Female',
                    'code_name': 'female'
                },
                {
                    'label': 'x',
                    'code_name': 'x'
                },
            ]
        },
        {
            'field':{
                'label': 'Date Of Expiry',
                'code_name': 'dateofexpiry',
                'kind': 2,
                'description': '',
                'is_fixed': True,
                'is_required': True,
                'is_required_error': 'This field is required!',
            },
            'sub_field': {
                'max_kind': 1,
                'max_now_delta': None,
                'max_date': None,
                'max_date_error': '',
                'min_kind': 2,
                'min_now_delta': timedelta(days=180),
                'min_date': None,
                'min_date_error': 'Minimum allowed date is [limit]'
            }
        }
    ]

    for item in items:
        field = Field.objects.create(
            **item['field']
        )
        if item['field']['kind'] == Field.KIND_TEXT:
            FieldText.objects.create(
                field=field,
                **item['sub_field']
            )
        elif item['field']['kind'] == Field.KIND_DATE:
            FieldDate.objects.create(
                field=field,
                **item['sub_field']
            )
        elif item['field']['kind'] == Field.KIND_CHOICES:
            for option in item['options']:
                FieldChoice.objects.create(
                    field=field,
                    is_deleted=False,
                    **option,
                )

class Migration(migrations.Migration):

    dependencies = [
        ('visa_field', '0012_field_is_fixed')
    ]

    operations = [
        migrations.RunPython(fixed_fields)
    ]
