from django.db import models


class Nationality(models.Model):
    class Meta:
        db_table = 'nationality'

    country = models.ForeignKey(
        'country.Country',
        on_delete=models.PROTECT,
        related_name='nationalities',
        related_query_name='nationalities'
    )
    is_active   = models.BooleanField(default=False)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class NationalityLocale(models.Model):
    class Meta:
        db_table = 'nationality_locale'

    nationality = models.ForeignKey(Nationality, on_delete=models.PROTECT)
    language    = models.ForeignKey('language.Language', on_delete=models.PROTECT)
    name        = models.CharField(max_length=200)
