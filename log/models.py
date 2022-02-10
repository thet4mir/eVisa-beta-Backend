from django.db import models
from django.conf import settings


class Log(models.Model):

    class Meta:
        db_table = "log"

    KIND_DELETE = 1
    KIND_UPDATE = 2
    KIND_CREATE = 3

    KIND = [
        (KIND_DELETE, "delete"),
        (KIND_UPDATE, "update"),
        (KIND_CREATE, "create"),
    ]

    model_name  = models.CharField(max_length=200)
    instance_id = models.PositiveIntegerField(null=True)
    payload     = models.JSONField(null=True)
    kind        = models.PositiveSmallIntegerField(choices=KIND, db_index=True, null=True)
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at  = models.DateTimeField(auto_now_add=True)

    """
    {
        'model_name': 'Country'
        'isntance_id': 4
        'payload': {
            'name': 'United States',
            'is_active': True,
            'code_alpha2': 'US',
            'code_alpha3': 'USA',
            'nationality': 'American',
            'code_numeric': '840'
        }
        'kind': 'KIND_CREATE'
        'modified_by': 'superuser'
    }
    """
