import csv

from django.http import HttpResponse
from django.views.generic.list import ListView, View
from django.shortcuts import render

from currency.models import Rate


# def rates(request):
#     queryset = Rate.objects.order_by('-created')[:20]
#     return render(request, 'rates_list.html', context={'rates': queryset})


class RateListView(ListView):
    model = Rate
    template_name = 'rate_list.html'
    paginate_by = 50
    ordering = '-created'
    # ordering = ('-id', '-source')


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
            writer.writerow(map(str, [
                rate.id,
                rate.created,
                rate.get_currency_display(),
                rate.buy,
                rate.sale,
                rate.get_source_display(),
            ]))

        return response
