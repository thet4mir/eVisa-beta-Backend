# Generated by Django 3.1.6 on 2021-03-04 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visa', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentfield',
            name='document',
        ),
        migrations.RemoveField(
            model_name='documentfield',
            name='field',
        ),
        migrations.RemoveField(
            model_name='fieldchoice',
            name='field',
        ),
        migrations.RemoveField(
            model_name='person',
            name='document',
        ),
        migrations.RemoveField(
            model_name='person',
            name='visa',
        ),
        migrations.RemoveField(
            model_name='valuetext',
            name='document_field',
        ),
        migrations.RemoveField(
            model_name='valuetext',
            name='person',
        ),
        migrations.RemoveField(
            model_name='visa',
            name='country',
        ),
        migrations.RemoveField(
            model_name='visa',
            name='visa_type',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='DocumentField',
        ),
        migrations.DeleteModel(
            name='Field',
        ),
        migrations.DeleteModel(
            name='FieldChoice',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.DeleteModel(
            name='ValueText',
        ),
        migrations.DeleteModel(
            name='Visa',
        ),
        migrations.DeleteModel(
            name='VisaType',
        ),
    ]
