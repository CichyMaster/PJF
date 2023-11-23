from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from PhoneService.forms import SearchForm, RejestrationForm
from PhoneService.models import Repairs, Phones, Workers


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
            return redirect(f'http://127.0.0.1:8000/PhoneService/Rejestracja')
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
            return redirect(f'http://127.0.0.1:8000/PhoneService/Wyszukiwanie/{search_value}')
    return render(request, "PhoneService/read.html", {"list_of_phones": list_of_phones, 'form': form})

def result_view_by_case(request, nr_case):
    repair = get_object_or_404(Repairs, nr_case=nr_case)
    return render(request, 'PhoneService/specific_case.html', {'repair': repair})

def result_view_by_IMEI(request, IMEI):
    repair = get_object_or_404(Repairs, imei=IMEI)
    return render(request, 'PhoneService/specific_case.html', {'repair': repair})

def edit(request):
    return render(request, 'PhoneService/edit.html')

def edit_by_IMEI(request, IMEI):
    repair = get_object_or_404(Repairs, imei=IMEI)
    return render(request, 'PhoneService/edit_case.html', {'repair': repair})

def edit_by_case(request, nr_case):
    repair = get_object_or_404(Repairs, nr_case=nr_case)
    return render(request, 'PhoneService/edit_case.html', {'repair': repair})

def delete(request):
    return HttpResponse("Strona do usuwania")


