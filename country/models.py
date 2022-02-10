from django.db import models
from language.models import Language


class Country(models.Model):

    class Meta:
        db_table = 'country'

    is_active   = models.BooleanField(default=False)

    code_alpha2 = models.CharField(max_length=5, db_index=True)
    code_alpha3 = models.CharField(max_length=5, db_index=True)
    code_numeric = models.CharField(max_length=5, db_index=True)

    deleted_at  = models.DateTimeField(null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def get_default_name(self):
        default_lang = Language.objects.filter(is_default=True).last()
        locales = self.locales.filter(language=default_lang)
        return locales.last().name


class CountryLocale(models.Model):

    class Meta:
        db_table = 'country_locale'

    country     = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='locales')
    language    = models.ForeignKey(Language, on_delete=models.PROTECT)
    name        = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200)
