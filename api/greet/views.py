"""
Django views
"""
import random

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

GREETED = ["GitHub", "GitHub Actions", "CICD", "AWS"]


@require_http_methods(["GET"])
def hello_view(request):
    greeted = random.choice(GREETED)
    return JsonResponse({"message": f"Hello, {greeted}!"})


@require_http_methods(["GET"])
def yell_view(request):
    greeted = random.choice(GREETED)
    return JsonResponse({"message": f"Hello, {greeted}!".upper()})


@require_http_methods(["GET"])
def whisper_view(request):
    greeted = random.choice(GREETED)
    return JsonResponse({"message": f"Hello, {greeted}".lower()})
