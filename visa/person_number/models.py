from django.db import models


class VisaPersonNumber(models.Model):

    class Meta:
        db_table = 'visa_person_number'

    ID_CHARS = "0123456789ACDEFGHJKLMNPRSTUVWXYZ"

    id = models.CharField(max_length=12, primary_key=True)
    length = models.PositiveSmallIntegerField(db_index=True)
    is_used = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
