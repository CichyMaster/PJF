from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from PhoneService.forms import SearchForm
from PhoneService.models import Repairs


def index(request):
    return render(request, "PhoneService/index.html")

def create(request):
    return HttpResponse("Stronka do rejestacji")

def read(request):
    list_of_phones = Repairs.objects.all().order_by('nr_case')
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_value = form.cleaned_data['search_value']
            return HttpResponseRedirect(f'http://127.0.0.1:8000/PhoneService/Wyszukiwanie/{search_value}')
    return render(request, "PhoneService/read.html", {"list_of_phones": list_of_phones, 'form': form})

def result_view_by_case(request, nr_case):
    repair = get_object_or_404(Repairs, nr_case=nr_case)
    return render(request, 'PhoneService/specific_case.html', {'repair': repair})

def result_view_by_IMEI(request, IMEI):
    repair = get_object_or_404(Repairs, imei=IMEI)
    return render(request, 'PhoneService/specific_case.html', {'repair': repair})

def edit(request):
    return HttpResponse("Strona do edycji")

def delete(request):
    return HttpResponse("Strona do usuwania")


