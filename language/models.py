from django.db import models


class Language(models.Model):

    class Meta:
        db_table = 'language'

    name        = models.CharField(max_length=100)
    name_local  = models.CharField(max_length=100)
    # XXX https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    code_name   = models.CharField(max_length=10, db_index=True)
    is_active   = models.BooleanField(default=False, db_index=True)
    is_default  = models.BooleanField(default=False, db_index=True)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
