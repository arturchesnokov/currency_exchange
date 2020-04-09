import csv

from django.core.cache import cache
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.list import ListView, View
from django_filters.views import FilterView
from django.shortcuts import render

from currency.models import Rate
from currency.filters import RateFilter
from urllib.parse import urlencode

from currency import model_choices as mch
from currency.utils import generate_rate_cache_key


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


class LatestRates(TemplateView):
    template_name = 'rates.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # rates = {
        #     'PrivatBank': [Rate.objects.filter(source=mch.SR_PRIVAT, currency=mch.CURR_USD).last(),
        #                    Rate.objects.filter(source=mch.SR_PRIVAT, currency=mch.CURR_EUR).last()]
        # }

        rates = []
        for bank in mch.SOURCE_CHOICES:
            source = bank[0]
            for curr in mch.CURRENCY_CHOICES:
                currency = curr[0]
                cache_key = generate_rate_cache_key(source, currency)

                rate = cache.get(cache_key)
                if rate is None:
                    rate = Rate.objects.filter(source=source, currency=currency).order_by('created').last()
                    if rate:
                        rate_dict = {
                            'currency': rate.get_currency_display(),
                            'source': rate.get_source_display(),
                            'sale': rate.sale,
                            'buy': rate.buy,
                            'created': rate.created,
                        }

                        rates.append(rate_dict)
                        cache.set(cache_key, rate_dict, 60 * 15)
                else:
                    rates.append(rate)

        context['rates'] = rates
        return context
