# Generated by Django 3.1.6 on 2021-03-15 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visa_kind', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visakind',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
    ]
