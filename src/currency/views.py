from django.views.generic.list import ListView
from django.shortcuts import render

from currency.models import Rate


# def rates(request):
#     queryset = Rate.objects.order_by('-created')[:20]
#     return render(request, 'rates_list.html', context={'rates': queryset})


class RateListView(ListView):
    model = Rate
    template_name = 'rate_list.html'
    paginate_by = 20

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     queryset = Rate.objects.all().order_by('-id')
    #     context['rates'] = queryset  # зачем указываем имя контектсу если в шаблоне используем object_list?
    #     return context

    def get_queryset(self):
        return Rate.objects.all().order_by('-id')
