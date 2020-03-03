from django.shortcuts import render

from currency.models import Rate


def rates(request):
    queryset = Rate.objects.all()
    return render(request, 'rates.html', context={'rates': queryset})
