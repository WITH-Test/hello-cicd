from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


def hello_view(request):
    return JsonResponse({"message": f"Hello, AWS!"})
