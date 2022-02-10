from django.db import models

"""
+--------+      +-------------+
| Field  +<-----+ FieldChoice |
+---+----+      +-------------+
"""


class Field(models.Model):

    class Meta:
        db_table = "field"

    KIND_TEXT = 1
    KIND_DATE = 2
    KIND_CHOICES = 3

    KIND = [
        (KIND_TEXT, "Text Field"),
        (KIND_DATE, "Date Field"),
        (KIND_CHOICES, "Choice Field"),
    ]

    label               = models.CharField(max_length=250)
    code_name           = models.CharField(max_length=50, db_index=True)
    kind                = models.PositiveSmallIntegerField(choices=KIND, db_index=True)
    description         = models.CharField(max_length=5000, null=True, blank=True)
    is_fixed            = models.BooleanField(default=False)
    is_required         = models.BooleanField(default=False)
    is_required_error   = models.CharField(max_length=2000, null=True)

    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    deleted_at          = models.DateTimeField(null=True)


class FieldChoice(models.Model):

    class Meta:
        db_table = "field_choice"

    field       = models.ForeignKey(Field, on_delete=models.PROTECT)
    label       = models.CharField(max_length=200)
    code_name   = models.CharField(max_length=50)
    is_deleted  = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class FieldText(models.Model):

    class Meta:
        db_table = "field_text"

    field = models.ForeignKey(Field, on_delete=models.PROTECT)

    min_length          = models.IntegerField(null=True, blank=True)
    min_length_error    = models.CharField(max_length=250, null=True, blank=True)

    max_length          = models.IntegerField(null=True, blank=True)
    max_length_error    = models.CharField(max_length=250, null=True, blank=True)

    regex_chars         = models.CharField(max_length=500, null=True, blank=True)
    regex_chars_error   = models.CharField(max_length=250, null=True, blank=True)


class FieldDate(models.Model):

    class Meta:
        db_table = "field_date"

    KIND_NONE = 1
    KIND_NOW = 2
    KIND_DATE = 3

    KIND_CHOICES = (
        (KIND_NONE, 'Байхгүй'),
        (KIND_NOW, '[Одоо]'),
        (KIND_DATE, 'Date'),
    )

    field = models.ForeignKey(Field, on_delete=models.PROTECT)

    max_kind        = models.PositiveSmallIntegerField(choices=KIND_CHOICES, db_index=True)
    max_now_delta   = models.DurationField(null=True, blank=True)
    max_date        = models.DateField(null=True, blank=True)
    max_date_error  = models.CharField(max_length=250, null=True, blank=True)

    min_kind        = models.PositiveSmallIntegerField(choices=KIND_CHOICES, db_index=True)
    min_now_delta   = models.DurationField(null=True, blank=True)
    min_date        = models.DateField(null=True, blank=True)
    min_date_error  = models.CharField(max_length=250, null=True, blank=True)
