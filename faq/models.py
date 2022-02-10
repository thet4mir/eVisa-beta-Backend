from django.db import models
from django.db.models import Max


class FaqManager(models.Manager):

    def get_next_sort_order(self):
        result = self.get_queryset().aggregate(Max('sort_order'))
        return result['sort_order__max'] + 1


class Faq(models.Model):

    class Meta:
        db_table = 'faq'
        ordering = ['sort_order']

    objects = FaqManager()

    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=4000, null=True)
    sort_order = models.SmallIntegerField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
