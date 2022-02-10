from django.db import models


class Config(models.Model):

    class Meta:
        db_table = 'config'

    name = models.CharField(max_length=250, unique=True)
    value = models.CharField(max_length=4000, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
