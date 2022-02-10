# Generated by Django 3.1.6 on 2021-03-25 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visa', '0005_valuechoice_valuedate'),
    ]

    operations = [
        migrations.AddField(
            model_name='visa',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='visa',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'New Request'), (2, 'Visa Approved'), (3, 'Visa Declined')], db_index=True, default=1),
        ),
        migrations.AlterField(
            model_name='visa',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]