# Generated by Django 3.1.6 on 2021-04-24 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visa_field', '0010_auto_20210323_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldchoice',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
