import csv

from django.http import HttpResponse
from django.views.generic.list import ListView, View
from django_filters.views import FilterView
from django.shortcuts import render

from currency.models import Rate
from currency.filters import RateFilter
from urllib.parse import urlencode


# def rates(request):
#     queryset = Rate.objects.order_by('-created')[:20]
#     return render(request, 'rates_list.html', context={'rates': queryset})


class RateListView(FilterView):
    model = Rate
    template_name = 'rate_list.html'
    paginate_by = 10
    ordering = '-created'
    filterset_class = RateFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        query_params = dict(self.request.GET.items())
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = urlencode(query_params)

        return context


# def get_paginate_by(self, queryset):
#     super().get_paginate_by()
#
# @property
# def paginate_by(self):
#     paginate = int(self.request.GET.get('paginate-by'))
#     return paginate


class RateCSV(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rates.csv"'
        writer = csv.writer(response)
        headers = [
            'id',
            'created',
            'currency',
            'buy',
            'sale',
            'source',
        ]
        writer.writerow(headers)
        for rate in Rate.objects.all().iterator():
            row = [
                getattr(rate, f'get_{attr}_display')() if hasattr(rate, f'get_{attr}_display')
                else getattr(rate, attr)
                for attr in headers]
            writer.writerow(row)

        return response
