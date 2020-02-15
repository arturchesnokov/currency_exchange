from django.shortcuts import render
from django.http import HttpResponse


def smoke(request):
    return HttpResponse('smoke')
