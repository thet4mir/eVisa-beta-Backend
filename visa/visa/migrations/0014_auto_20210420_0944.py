# Generated by Django 3.1.6 on 2021-04-20 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visa', '0013_auto_20210420_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valuetext',
            name='value',
            field=models.CharField(blank=True, max_length=4000, null=True),
        ),
    ]