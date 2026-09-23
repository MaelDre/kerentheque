from django.urls import path

from . import views

app_name = "moderation"

urlpatterns = [
    path("objets/<int:item_pk>/signaler/", views.report, name="report"),
]
