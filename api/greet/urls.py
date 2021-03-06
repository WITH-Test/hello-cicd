from django.urls import path

from .views import hello_view, yell_view

urlpatterns = [
    path(r"", hello_view, name="greet-people"),
    path(r"louder", yell_view, name="yell-at-people"),
]
