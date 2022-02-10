from main.forms import BaseModelForm

from .models import Country, CountryLocale


class LocaleForm(BaseModelForm):

    class Meta:
        model = CountryLocale

        fields = ('name', 'nationality')


class CountryForm(BaseModelForm):

    class Meta:
        model = Country

        fields = (
            'is_active',
            'code_alpha2',
            'code_alpha3',
            'code_numeric',
        )
