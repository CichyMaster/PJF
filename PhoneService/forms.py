from django import forms


class SearchForm(forms.Form):
    search_value = forms.CharField(label='Numer przypadku', max_length=17)