# Generated by Django 3.1.6 on 2021-02-23 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0001_initial'),
        ('country', '0002_remove_country_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CountryTranslation',
            new_name='CountryLocale',
        ),
    ]
