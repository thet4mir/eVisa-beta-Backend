# Generated by Django 3.1.6 on 2021-02-06 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='value',
            field=models.CharField(max_length=4000, null=True),
        ),
    ]