# Generated by Django 3.1.6 on 2021-02-23 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0004_auto_20210223_2016'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='country',
            table='country',
        ),
        migrations.AlterModelTable(
            name='countrylocale',
            table='country_locale',
        ),
    ]
