"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from config.views import status

admin.site.site_header = "Civil Legal Advice Administration"
admin.site.site_title = "CLA Admin"
admin.site.index_title = "Manage CLA services"


# `/admin` path should always be at the lowest priority to avoid conflicts with other apps that may use the `/admin` path.
urlpatterns = [
    path("admin/reports/", include("apps.reports.urls")),
    path("admin/", admin.site.urls),
    path("status", status, name="status"),
]
