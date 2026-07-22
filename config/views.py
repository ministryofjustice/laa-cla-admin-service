from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def status(_request):
    return JsonResponse({"status": "ok"})
