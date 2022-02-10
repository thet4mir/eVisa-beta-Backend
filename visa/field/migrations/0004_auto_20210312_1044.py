# Generated by Django 3.1.6 on 2021-03-12 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visa_field', '0003_auto_20210312_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='kind',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Text Field'), (2, 'Date Field'), (3, 'Choice Field')], db_index=True),
        ),
    ]
