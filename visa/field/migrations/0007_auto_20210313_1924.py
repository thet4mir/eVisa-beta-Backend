# Generated by Django 3.1.6 on 2021-03-13 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visa_field', '0006_auto_20210313_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldchoice',
            name='code_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]