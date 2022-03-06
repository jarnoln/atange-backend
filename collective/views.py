from django.http import HttpResponse
from django.shortcuts import render

from .models import Collective


def index(request):
    collectives = Collective.objects.all()
    context = {'collectives': collectives}
    return render(request, 'collective/index.html', context)


def collective(request, collective_name):
    return HttpResponse('Collective: {}'.format(collective_name))
