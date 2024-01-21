import base64
from datetime import datetime, date
from io import BytesIO

from django.shortcuts import render, redirect
from PhoneService.forms import SearchForm, RejestrationForm, EditionForm, DeleteForm
from PhoneService.models import Repairs, Phones, Workers
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')


def index(request):
    return render(request, "PhoneService/index.html")


def create(request):
    if request.method == 'POST':
        form = RejestrationForm(request.POST)
        if form.is_valid():
            nr_case = form.cleaned_data['nr_case']
            imei = form.cleaned_data['imei']
            status = form.cleaned_data['status']
            operator = form.cleaned_data['operator']
            admission_date = form.cleaned_data['admission_date']
            model = form.cleaned_data['model']
            workers = form.cleaned_data['workers']
            repair = Repairs(
                nr_case=nr_case,
                imei=imei,
                status=status,
                operator=operator,
                admission_date=admission_date,
                id_phone=Phones.objects.get(model=model),
                id_worker=Workers.objects.get(acronym=workers),
            )
            repair.save()
            return redirect(f'../Rejestracja')
    else:
        form = RejestrationForm()
    return render(request, 'PhoneService/create.html', {'form': form})


def read(request):
    list_of_phones = Repairs.objects.all().order_by('nr_case')
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_value = form.cleaned_data['search_value']
            return redirect(f'../Wyszukiwanie/{search_value}')
    return render(request, "PhoneService/read.html", {"list_of_phones": list_of_phones, 'form': form})


def result_view_by_case(request, nr_case):
    repair = Repairs.objects.filter(nr_case=nr_case)
    return render(request, 'PhoneService/specific_case.html', {'repair': repair})


def result_view_by_imei(request, imei):
    repair = Repairs.objects.filter(imei=imei)
    print(repair)
    return render(request, 'PhoneService/specific_case.html', {'repair': repair})


def edit(request):
    form = EditionForm()
    if request.method == 'POST':
        form = EditionForm(request.POST)
        if 'fill_values' in request.POST:
            if form.is_valid():
                search_value = form.cleaned_data['search_value']
                repair = Repairs.objects.filter(nr_case=search_value).first()
                if repair:
                    form = EditionForm(initial={
                        'nr_case': repair.nr_case,
                        'imei': repair.imei,
                        'status': repair.status,
                        'operator': repair.operator,
                        'admission_date': repair.admission_date,
                        'end_date': repair.end_date,
                        'model': repair.id_phone,
                        'workers': repair.id_worker,
                    })
        elif 'update_record' in request.POST:
            if form.is_valid():
                search_value = form.cleaned_data['nr_case']
                repair = Repairs.objects.filter(nr_case=search_value).first()
                phone = Phones.objects.get(model=form.cleaned_data['model'])
                worker = Workers.objects.get(acronym=form.cleaned_data['workers'])
                if repair:
                    repair.nr_case = form.cleaned_data['nr_case']
                    repair.imei = form.cleaned_data['imei']
                    repair.status = form.cleaned_data['status']
                    repair.operator = form.cleaned_data['operator']
                    repair.admission_date = form.cleaned_data['admission_date']
                    repair.end_date = form.cleaned_data['end_date']
                    repair.id_phone = phone
                    repair.id_worker = worker
                    if repair.admission_date is not None and repair.end_date is not None:
                        if repair.admission_date > repair.end_date:
                            raise ValueError("Data przyjęcia jest później niż data zakonczenia")
                    repair.save()
                    return redirect(f'../Edycja/')
        elif 'add-end-date' in request.POST:
            if form.is_valid():
                mutable_data = request.POST.copy()
                mutable_data['end_date'] = date.today().strftime('%Y-%m-%d')
                form = EditionForm(mutable_data, initial=form.initial)
    return render(request, "PhoneService/edit.html", {"form": form})


def delete(request):
    form = DeleteForm()
    repair = None

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            search_value = form.cleaned_data['search_value']
            if 'search-button' in request.POST:
                if search_value:
                    repair = Repairs.objects.filter(nr_case=search_value).first()
            elif 'delete-button' in request.POST:
                if search_value:
                    repair = Repairs.objects.filter(nr_case=search_value).first()
                    if repair:
                        repair.delete()
                        return redirect(f'../Usuwanie/')

    return render(request, "PhoneService/delete.html", {"repair": repair, 'form': form})


def save_chart():
    # Zapisanie wykresu jako obrazek
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return image_png


def statistic(request):
    if request.method == 'POST':
        if 'Chart1' in request.POST:
            workers_acronyms = Workers.objects.all().order_by('acronym').values_list('acronym', flat=True)
            workers_dict = {}

            for worker in workers_acronyms:
                workers_dict[worker] = 0
            today = datetime.now().date()
            if today.month == 1:
                last_month_repairs = Repairs.objects.filter(end_date__year=today.year - 1, end_date__month=12)
            else:
                last_month_repairs = Repairs.objects.filter(end_date__year=today.year, end_date__month=today.month - 1)

            for worker in last_month_repairs:
                if worker.id_worker.acronym:
                    workers_dict[worker.id_worker.acronym] += 1

            label_of_workers = list(workers_dict.keys())
            label_of_values = list(workers_dict.values())

            # Tworzenie wykresu
            plt.bar(label_of_workers, label_of_values)
            plt.xlabel('Pracownicy')
            plt.ylabel('Liczba zakonczonych telefonów')
            plt.title('Rozkład zakończonych telefonów z ostatniego miesiąca')

            # Konwersja obrazka na base64 (wersje odczytywalną przez przegladarkę)
            graphic = base64.b64encode(save_chart()).decode('utf-8')
            plt.clf()
            # przekazanie wykresu do szablonu
            context = {'graphic': graphic}
        elif 'Chart2' in request.POST:

            all_repairs = Repairs.objects.all()
            repairs_dict = {'Naprawa': 0, 'Reklamacja': 0, 'Gwarancyjna': 0}

            for repair in all_repairs:
                repairs_dict[repair.status] += 1

            label_of_statuses = list(repairs_dict.keys())
            label_of_repairs = list(repairs_dict.values())

            # Tworzenie wykresu
            plt.pie(label_of_repairs, labels=label_of_statuses, autopct='%1.1f%%')
            plt.title('Rozkład dokonanych napraw względem rodzaju naprawy')

            # Konwersja obrazka na base64
            graphic = base64.b64encode(save_chart()).decode('utf-8')
            plt.clf()
            # przekazanie wykresu do szablonu
            context = {'graphic': graphic}

    else:
        context = {'graphic': 'Nie wybrano wykresu'}
    return render(request, "PhoneService/statistics.html", context)
