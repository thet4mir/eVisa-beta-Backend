# Generated by Django 3.1.6 on 2021-02-23 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0003_auto_20210223_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrylocale',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='locales', to='country.country'),
        ),
    ]
