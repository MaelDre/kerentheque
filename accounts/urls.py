from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "accounts"

urlpatterns = [
    path("connexion/", views.login_request, name="login"),
    path("connexion/lien/", views.magic_link, name="magic_link"),
    path("deconnexion/", LogoutView.as_view(), name="logout"),
    path("profil/", views.profile, name="profile"),
    path("profil/supprimer/", views.delete_account_view, name="delete"),
    path("mentions-legales/", TemplateView.as_view(template_name="accounts/legal.html"), name="legal"),
    path("confidentialite/", TemplateView.as_view(template_name="accounts/privacy.html"), name="privacy"),
]
