from django.contrib import admin
from django.shortcuts import render

from apps.cla_auth.models import User


def index(request):
    context = {
        **admin.site.each_context(request),
        "title": "Reports",
    }

    return render(
        request,
        "admin/reports/index.html",
        context,
    )


def users_report(request):
    users = User.objects.all().order_by("username")
    context = {
        **admin.site.each_context(request),
        "title": "Users report",
        "users": users,
    }

    return render(
        request,
        "admin/reports/users_report.html",
        context,
    )
