from django.db import migrations, models


def copy_name_to_nationality(apps, schema_editor):
    CountryLocale = apps.get_model('country', 'CountryLocale')

    locales = CountryLocale.objects.all()
    for locale in locales:
        locale.nationality = locale.name
        locale.save()


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0005_auto_20210223_2026'),
        ('nationality', '0003_auto_20210302_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrylocale',
            name='nationality',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.RunPython(copy_name_to_nationality),
    ]
