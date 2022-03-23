"""
Django views
"""
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

@require_http_methods(["GET"])
def hello_view(request):
    return JsonResponse({"message": f"Hello, CodeClimate?"})
