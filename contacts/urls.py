from django.urls import path

from . import views

app_name = "contacts"

urlpatterns = [
    path("objets/<int:item_pk>/demander/", views.send, name="send"),
    path("mes-demandes/", views.sent, name="sent"),
    path("demandes-recues/", views.received, name="received"),
    path("demandes-recues/<int:pk>/accepter/", views.accept, name="accept"),
    path("demandes-recues/<int:pk>/refuser/", views.refuse, name="refuse"),
]
