import csv

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render

from apps.cla_auth.models import User


@staff_member_required
def index(request):
    reports = [
        {"name": "Users", "description": "List of all users", "url": "reports:users"},
    ]
    return render(request, "admin/reports/index.html", {"reports": reports})


@staff_member_required
def users(request):
    queryset = User.objects.order_by("username").values(
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "date_joined",
        "last_login",
    )

    if request.GET.get("format") == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="users.csv"'
        writer = csv.DictWriter(
            response, fieldnames=list(queryset[0].keys()) if queryset else []
        )
        writer.writeheader()
        writer.writerows(queryset)
        return response

    return render(request, "admin/reports/users.html", {"users": queryset})
