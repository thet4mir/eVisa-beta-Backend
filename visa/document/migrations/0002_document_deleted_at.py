# Generated by Django 3.1.6 on 2021-03-14 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visa_document', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
    ]
