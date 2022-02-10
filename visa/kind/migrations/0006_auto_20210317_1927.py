# Generated by Django 3.1.6 on 2021-03-17 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0006_countrylocale_nationality'),
        ('visa_kind', '0005_auto_20210317_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='visakind',
            name='fee_exempt_country',
            field=models.ManyToManyField(related_name='visa_fee_exempt_country', through='visa_kind.VisaFeeExemptCountry', to='country.Country'),
        ),
        migrations.AlterField(
            model_name='visakind',
            name='visa_exempt_country',
            field=models.ManyToManyField(related_name='visa_exempt_country', through='visa_kind.VisaExemptCountry', to='country.Country'),
        ),
    ]