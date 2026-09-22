from django.contrib import admin
from django.shortcuts import redirect, reverse


class AdminSite(admin.AdminSite):
    site_header = "Civil Legal Advice Administration"
    site_title = "CLA Admin"
    index_title = "Manage CLA services"

    def logout(self, request, extra_context=...):
        return redirect(reverse("django_entra_auth:logout"))


admin_site = AdminSite(name="cla-admin")
