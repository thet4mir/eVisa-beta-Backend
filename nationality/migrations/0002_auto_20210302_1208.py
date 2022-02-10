# Generated by Django 3.1.6 on 2021-03-02 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0005_auto_20210223_2026'),
        ('nationality', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nationality',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nationalities', to='country.country'),
        ),
    ]