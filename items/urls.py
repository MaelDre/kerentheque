from django.urls import path

from . import views

app_name = "items"

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("objets/<int:pk>/", views.detail, name="detail"),
    path("mes-objets/", views.mine, name="mine"),
    path("mes-objets/ajouter/", views.create, name="create"),
    path("mes-objets/<int:pk>/modifier/", views.edit, name="edit"),
    path("mes-objets/<int:pk>/supprimer/", views.delete, name="delete"),
]
