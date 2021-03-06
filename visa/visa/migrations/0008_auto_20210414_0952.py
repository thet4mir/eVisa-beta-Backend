# Generated by Django 3.1.6 on 2021-04-14 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visa_field', '0010_auto_20210323_1901'),
        ('visa', '0007_auto_20210412_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valuechoice',
            name='value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='visa_field.fieldchoice'),
        ),
        migrations.AlterField(
            model_name='valuedate',
            name='value',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='valuetext',
            name='value',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
