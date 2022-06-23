from django.shortcuts import render
from django.contrib.auth.models import User
from django.conf import settings
from collective.models import Statistics


def index(request):
    statistics = Statistics.objects.order_by("-created")
    users = User.objects.order_by("username")
    context = {"settings": settings, "statistics": statistics, "users": users}
    return render(request, "collective/index.html", context)
