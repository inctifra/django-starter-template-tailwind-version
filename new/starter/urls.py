from django.urls import path

from labb.shortcuts import set_theme_view

from . import views

app_name = "starter"

urlpatterns = [
    path("", views.index, name="index"),
    path("set-theme/", set_theme_view, name="set_theme"),
]
