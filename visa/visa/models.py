from django.db import models
from django.conf import settings
from visa.kind.models import VisaKind


"""
                                                        +--------------------+      +-------------+
                                                        |       Field        +<-----+ FieldChoice |
                                                        +---------+----------+      +-------------+
                                                                  ^
                                                                  |
                                                                  |
                                                                  |
                                                                  |
                      +--------------------+            +---------+----------+
                      |     Document       +<-----------+    DocumentField   +<----+
                      +---------+-----+----+            +--------------------+     |
                                ^     ^                                            |
                                |     |                 +--------------------+     |
                                |     +-----------------+  DocumentCountry   |     |
                                |                       +---------+----------+     |
                                |                                                  |
+--------------+      +--------------------+                                       |
|   VisaKind   +<-----+  VisaKindDocument  |                                       |
+-------+------+      +--------------------+                                       |
        ^                                                                          |
        |                                                                          |
        |                                                                          |
        |                                                                          |
+-------+------+       +--------------------+           +--------------------+     |
|     Visa     +<------+    Person          +<----------+    ValueText       +-----+
+--------------+       +------+----+--------+           +--------------------+
                                    ^    ^
                                    |    |              +--------------------+
                                    |    +--------------+   ValueChoice      |
                                    |                   +--------------------+
                                    |
                                    |                   +--------------------+
                                    +-------------------+   ValueNationality |
                                                        +--------------------+
"""


class Visa(models.Model):

    class Meta:
        db_table = "visa"

    visa_kind       = models.ForeignKey('visa_kind.VisaKind', on_delete=models.PROTECT)
    country         = models.ForeignKey('country.Country', on_delete=models.PROTECT)

    date_of_arrival = models.DateTimeField()
    days_stay       = models.PositiveSmallIntegerField()
    days_valid      = models.PositiveSmallIntegerField()
    entry_kind      = models.PositiveSmallIntegerField(choices=VisaKind.ENTRY_KIND_CHOICES, db_index=True)
    fee_person      = models.DecimalField(max_digits=13, decimal_places=2)

    created_by      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="created_by"
    )
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)


class Person(models.Model):

    class Meta:
        db_table = "person"

    STATUS_NEW = 1
    STATUS_APPROVE = 2
    STATUS_DECLINE = 3

    STATUS = [
        (STATUS_NEW, "New Request"),
        (STATUS_APPROVE, "Visa Approved"),
        (STATUS_DECLINE, "Visa Declined"),
    ]

    visa            = models.ForeignKey(Visa, on_delete=models.PROTECT)
    number          = models.CharField(max_length=12, unique=True)
    document        = models.ForeignKey('visa_document.Document', on_delete=models.PROTECT)
    status          = models.PositiveSmallIntegerField(choices=STATUS, db_index=True, default=STATUS_NEW)
    updated_by   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        related_name="modified_by"
    )

    image_portrait  = models.ImageField(upload_to='image_portrait')
    image_document  = models.ImageField(upload_to='image_document')

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)


class ValueText(models.Model):

    class Meta:
        db_table = "value_text"

    person          = models.ForeignKey(Person, on_delete=models.PROTECT)
    document_field  = models.ForeignKey('visa_document.DocumentField', on_delete=models.PROTECT)
    value           = models.CharField(max_length=4000, null=True, blank=True)


class ValueDate(models.Model):

    class Meta:
        db_table = 'value_date'

    person          = models.ForeignKey(Person, on_delete=models.PROTECT)
    document_field  = models.ForeignKey('visa_document.DocumentField', on_delete=models.PROTECT)
    value           = models.DateTimeField(null=True, blank=True)


class ValueChoice(models.Model):

    class Meta:
        db_table = 'value_choice'

    person          = models.ForeignKey(Person, on_delete=models.PROTECT)
    document_field  = models.ForeignKey('visa_document.DocumentField', on_delete=models.PROTECT)
    value           = models.ForeignKey('visa_field.FieldChoice', on_delete=models.PROTECT, null=True, blank=True)
