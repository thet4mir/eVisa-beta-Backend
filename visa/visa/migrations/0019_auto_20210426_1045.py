# Generated by Django 3.1.6 on 2021-04-26 10:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visa', '0018_auto_20210421_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='created_by',
        ),
        migrations.AddField(
            model_name='visa',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
