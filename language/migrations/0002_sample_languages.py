from django.db import migrations


def sample_languages(apps, schema_editor):
    Language = apps.get_model('language', 'Language')

    items = [
        {
            'name': 'Англи',
            'name_local': 'English',
            'code_name': 'en',
            'is_default': True,
        },
        {
            'name': 'Орос',
            'name_local': 'Русский',
            'code_name': 'ru',
            'is_default': False,
        },
        {
            'name': 'Хятад',
            'name_local': '中文',
            'code_name': 'zh',
            'is_default': False,
        },
        {
            'name': 'Солонгос',
            'name_local': '한국어',
            'code_name': 'ko',
            'is_default': False,
        },
        {
            'name': 'Испани',
            'name_local': 'Español',
            'code_name': 'es',
            'is_default': False,
        },
    ]

    for item in items:
        Language.objects.create(
            is_active=True,
            **item,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(sample_languages),
    ]
