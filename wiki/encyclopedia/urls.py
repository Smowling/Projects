from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("error", views.error, name="error"),
    path("newentry", views.newentry, name="newentry"),
    path("edit/<str:page>", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("wiki/<str:page>", views.wikipage, name="wikipage"),
]
