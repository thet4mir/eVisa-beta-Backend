from django.db.models import Q, CharField
from django.db.models.functions import Lower
from .forms import VisaFilterForm
from .models import ValueText


class VisaFilter():

    def __init__(self, initial_queryset, form):
        assert isinstance(form, VisaFilterForm)
        self.qs = initial_queryset
        self.form = form
        self.value_list = ValueText.objects.filter(
            Q(document_field__field__code_name='name') |
            Q(document_field__field__code_name='surname')
        )
        CharField.register_lookup(Lower, "lower")

    def filter(self):

        form = self.form
        qs = self.qs
        value_list = self.value_list

        values = form.initial
        if form.is_bound:
            if form.is_valid():
                values = form.cleaned_data

        if values.get('status'):
            qs = qs.filter(status=values.get('status'))

        if values.get('kind'):
            qs = qs.filter(visa__visa_kind=values.get('kind'))

        if values.get('country'):
            qs = qs.filter(visa__country=values.get('country'))

        q_created = False
        if values.get('start_date'):
            q_created = Q(visa__created_at__gte=values.get('start_date'))
        if values.get('end_date'):
            end_date = values.get('end_date')
            if q_created:
                qs = qs.filter(q_created & Q(visa__created_at__lt=end_date))
            else:
                qs = qs.filter(visa__created_at__lt=end_date)
        else:
            if q_created:
                qs = qs.filter(q_created)

        qs_text = Q()
        if values.get('text'):
            texts = values.get('text').split()
            for text in texts:
                text = text.lower()
                filtered_list = value_list.filter(value__lower__icontains=text)
                list_person = [
                    person.person.id
                    for person in filtered_list
                ]
                qs_text = qs_text & (
                    Q(visa__created_by__email__lower__icontains=text) |
                    Q(number__icontains=text) |
                    Q(updated_by__email__icontains=text) |
                    Q(id__in=list_person)
                )
        if qs_text:
            qs = qs.filter(qs_text)

        return qs
