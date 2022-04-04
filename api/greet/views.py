"""
Django views
"""
import random

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

GREETED = ["GitHub", "GitHub Actions", "CICD", "WITH"]


@require_http_methods(["GET"])
def hello_view(request):
    greeted = random.choice(GREETED)
    return JsonResponse({"message": f"Hello, {greeted}!"})
