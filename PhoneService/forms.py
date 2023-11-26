import datetime

from django import forms

from PhoneService.models import Phones, Workers, Repairs


class SearchForm(forms.Form):
    search_value = forms.CharField(label='Numer przypadku lub IMEI', max_length=17)


class RejestrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RejestrationForm, self).__init__(*args, **kwargs)
        last_case = Repairs.objects.all().order_by('nr_case').last()
        prefix = last_case.nr_case[:3] if last_case and last_case.nr_case.startswith('DCR') else 'DCR'
        number = int(last_case.nr_case[3:]) + 1 if last_case and last_case.nr_case[3:].isdigit() else 1
        self.fields['nr_case'].initial = f"{prefix}{number:06d}"

    STATUS_CHOICES = (
        ("Naprawa", "Naprawa"),
        ("Gwarancyjna", "Gwarancyjna"),
        ("Reklamacja", "Reklamacja"),
    )
    list_of_models = Phones.objects.all().values_list('model', 'model')
    list_of_workers = Workers.objects.all().values_list('acronym', 'acronym')

    nr_case = forms.CharField(label='Numer przypadku:', max_length=9, disabled=True)
    imei = forms.IntegerField(label='IMEI:', max_value=99999999999999999)
    status = forms.ChoiceField(label='Rodzaj naprawy:', choices=STATUS_CHOICES, initial='Naprawa', required=True)
    operator = forms.CharField(label='Operator:', max_length=50)
    admission_date = forms.DateField(label='Data przyjęcia:', initial=datetime.date.today())
    model = forms.ChoiceField(label='Model telefonu:', choices=list_of_models)
    workers = forms.ChoiceField(label='Technik:', choices=list_of_workers)

class EditionForm(forms.Form):
    search_value = forms.CharField(label='Numer przypadku', max_length=9, required=False)

    STATUS_CHOICES = (
        ("Naprawa", "Naprawa"),
        ("Gwarancyjna", "Gwarancyjna"),
        ("Reklamacja", "Reklamacja"),
    )
    list_of_models = Phones.objects.all().values_list('model', 'model')
    list_of_workers = Workers.objects.all().values_list('acronym', 'acronym')

    nr_case = forms.CharField(label='Numer przypadku:', max_length=9, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    imei = forms.IntegerField(label='IMEI:', max_value=99999999999999999, required=False)
    status = forms.ChoiceField(label='Rodzaj naprawy:', choices=STATUS_CHOICES, required=False)
    operator = forms.CharField(label='Operator:', max_length=50, required=False)
    admission_date = forms.DateField(label='Data przyjęcia:', required=False)
    end_date = forms.DateField(label='Data zakończenia:', required=False)
    model = forms.ChoiceField(label='Model telefonu:', choices=list_of_models, required=False)
    workers = forms.ChoiceField(label='Technik:', choices=list_of_workers, required=False)

class DeleteForm(forms.Form):
    search_value = forms.CharField(label='Numer przypadku', max_length=9, required=False)


