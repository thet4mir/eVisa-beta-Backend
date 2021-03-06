# Generated by Django 3.1.6 on 2021-05-02 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0009_auto_20210408_1136'),
        ('visa', '0020_valuenationality'),
    ]

    operations = [
        migrations.AddField(
            model_name='valuenationality',
            name='value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='country.country'),
        ),
        migrations.AlterField(
            model_name='valuenationality',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='visa.person'),
        ),
    ]
