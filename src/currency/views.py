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
    paginate_by = 20
    ordering = '-id'
    # ordering = ('-id', '-source')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     queryset = Rate.objects.all().order_by('-id')
    #     context['rates'] = queryset  # зачем указываем имя контектсу если в шаблоне используем object_list?
    #     return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.order_by('-id')
        # return Rate.objects.all().order_by('-id')


"""
    created = models.DateTimeField(auto_now_add=True)
    currency = models.PositiveSmallIntegerField(choices=mch.CURRENCY_CHOICES)
    buy = models.DecimalField(max_digits=4, decimal_places=2)
    sale = models.DecimalField(max_digits=4, decimal_places=2)
    source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)
"""


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
