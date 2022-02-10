from django.db import models


class VisaKind(models.Model):
    """ Визийн ангилал """

    class Meta:
        db_table = "visa_kind"

    ENTRY_KIND_SINGLE = 1
    ENTRY_KIND_MULTIPLE = 2
    ENTRY_KIND_DOUBLE = 3

    ENTRY_KIND_CHOICES = [
        (ENTRY_KIND_SINGLE, "Single entry"),
        (ENTRY_KIND_DOUBLE, "Double entry"),
        (ENTRY_KIND_MULTIPLE, "Multiple entry"),
    ]

    title       = models.CharField(max_length=250)
    description = models.TextField()
    code_name   = models.CharField(max_length=5)
    is_active   = models.BooleanField()
    days_stay   = models.PositiveSmallIntegerField()
    days_valid  = models.PositiveSmallIntegerField()
    entry_kind  = models.PositiveSmallIntegerField(choices=ENTRY_KIND_CHOICES, db_index=True)
    fee_person  = models.DecimalField(max_digits=13, decimal_places=2)
    documents   = models.ManyToManyField(
        'visa_document.Document',
        through='VisaKindDocument'
    )
    visa_exempt_country = models.ManyToManyField(
        'country.Country',
        through='VisaExemptCountry',
        blank=True,
        related_name="visa_exempt_country"
    )
    fee_exempt_country = models.ManyToManyField(
        'country.Country',
        through='VisaFeeExemptCountry',
        blank=True,
        related_name="visa_fee_exempt_country"
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    deleted_at  = models.DateTimeField(null=True)


class VisaKindDocument(models.Model):
    """ Тухайн төрлийн виз ямар төрлийн баримт бичгүүд зөвшөөрдөг """

    class Meta:
        db_table = "visa_kind_document"

    visa_kind   = models.ForeignKey(VisaKind, on_delete=models.PROTECT)
    document    = models.ForeignKey(
        'visa_document.Document',
        on_delete=models.PROTECT,
        limit_choices_to={'is_active': True},
    )

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class VisaExemptCountry(models.Model):

    class Meta:
        db_table = 'visa_exempt_country'

    visa_kind   = models.ForeignKey(VisaKind, on_delete=models.PROTECT)
    country     = models.ForeignKey(
        'country.Country',
        on_delete=models.PROTECT,
        limit_choices_to={'is_active': True},
    )

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class VisaFeeExemptCountry(models.Model):

    class Meta:
        db_table = 'visafee_exempt_country'

    visa_kind   = models.ForeignKey(VisaKind, on_delete=models.PROTECT)
    country     = models.ForeignKey(
        'country.Country',
        on_delete=models.PROTECT,
        limit_choices_to={'is_active': True},
    )

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class VisaKindDiscount(models.Model):

    class Meta:
        db_table = 'visa_kind_discount'

    visa_kind   = models.ForeignKey(VisaKind, on_delete=models.PROTECT)
    num_person  = models.PositiveSmallIntegerField()
    percent     = models.DecimalField(max_digits=5, decimal_places=2)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
