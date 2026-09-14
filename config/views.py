from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET


@require_GET
def status(_request):
    return JsonResponse({"status": "ok"})


@require_GET
def home(_request):
    return redirect("/admin")
