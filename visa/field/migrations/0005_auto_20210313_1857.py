# Generated by Django 3.1.6 on 2021-03-13 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visa_field', '0004_auto_20210312_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fielddate',
            name='max_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fielddate',
            name='max_message',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='fielddate',
            name='max_now_delta',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fielddate',
            name='min_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fielddate',
            name='min_message',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='fielddate',
            name='min_now_delta',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
