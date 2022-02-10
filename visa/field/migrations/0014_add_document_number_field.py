from datetime import timedelta
from django.db import migrations
from visa.field.models import Field, FieldChoice, FieldDate, FieldText


def fixed_fields(apps, schema_editor):

    items = [
        {
            'field':{
                'label': 'Passport number',
                'code_name': 'documentnumber',
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
        ('visa_field', '0013_auto_20210504_1554')
    ]

    operations = [
        migrations.RunPython(fixed_fields)
    ]
