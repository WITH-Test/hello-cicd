"""
Django views
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def hello_view(request):
    return JsonResponse({"message": f"Hello, CodeClimate?"})
