# Generated by Django 3.1.6 on 2021-04-08 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=200)),
                ('instance_id', models.PositiveIntegerField(null=True)),
                ('payload', models.JSONField(null=True)),
                ('kind', models.PositiveSmallIntegerField(choices=[(1, 'delete'), (2, 'update'), (3, 'create')], db_index=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'log',
            },
        ),
    ]
