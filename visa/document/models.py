from django.db import models
from django.db.models import Max


class Document(models.Model):

    class Meta:
        db_table = "document"

    name            = models.CharField(max_length=250)
    is_active       = models.BooleanField(default=False)
    document_field  = models.ManyToManyField('visa_field.Field', through='DocumentField')

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    deleted_at      = models.DateTimeField(null=True)


class DocumentFieldManager(models.Manager):

    def get_next_sort_order(self):
        result = self.get_queryset().aggregate(Max('sort_order'))
        return result['sort_order__max'] + 1


class DocumentField(models.Model):

    class Meta:
        db_table = "document_field"
        ordering = ['sort_order']

    objects = DocumentFieldManager()

    document    = models.ForeignKey(Document, on_delete=models.PROTECT)
    field       = models.ForeignKey('visa_field.Field', on_delete=models.PROTECT)
    sort_order = models.PositiveSmallIntegerField(default=0)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class DocumentCountry(models.Model):
    """ Уг баримт бичгээр ямар улсын иргэнийг зөвшөөрөх """

    class Meta:
        db_table = "document_country"

    document    = models.ForeignKey(Document, on_delete=models.PROTECT)
    country     = models.ForeignKey('country.Country', on_delete=models.PROTECT)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
