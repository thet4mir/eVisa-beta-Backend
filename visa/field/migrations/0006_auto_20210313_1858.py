# Generated by Django 3.1.6 on 2021-03-13 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visa_field', '0005_auto_20210313_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldtext',
            name='max_length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fieldtext',
            name='max_length_error',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='fieldtext',
            name='min_length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fieldtext',
            name='min_length_error',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='fieldtext',
            name='regex_chars',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='fieldtext',
            name='regex_chars_error',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
