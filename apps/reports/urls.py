from django.contrib import admin
from django.urls import path

from . import views


app_name = "reports"


urlpatterns = [
    path(
        "",
        admin.site.admin_view(views.index),
        name="index",
    ),
    path(
        "users/",
        admin.site.admin_view(views.users_report),
        name="users_report",
    ),
]
