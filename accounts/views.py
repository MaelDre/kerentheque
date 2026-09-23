import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from sesame.utils import get_query_string, get_user

from .forms import LoginForm, ProfileForm
from .models import User
from .services import delete_account

logger = logging.getLogger(__name__)

LOGIN_LINK_THROTTLE_SECONDS = 60


def _send_login_link(email):
    # Au plus un envoi par email et par minute, pour éviter l'inondation d'une boîte mail.
    if not cache.add(f"login-link:{email}", True, LOGIN_LINK_THROTTLE_SECONDS):
        return
    user = User.objects.filter(email=email).first()
    if user is None:
        user = User.objects.create_user(email)
    if not user.is_active:
        return  # compte suspendu : aucun lien envoyé, sans le révéler
    link = settings.SITE_URL + reverse("accounts:magic_link") + get_query_string(user)
    body = render_to_string("accounts/emails/login_link.txt", {"link": link})
    try:
        send_mail("Votre lien de connexion à Kerentheque", body, None, [email])
    except Exception:
        logger.exception("Échec de l'envoi du lien de connexion")


@require_http_methods(["GET", "POST"])
def login_request(request):
    if request.user.is_authenticated:
        return redirect("items:catalog")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        _send_login_link(email)
        # Même réponse que le compte existe ou non.
        return render(request, "accounts/login_sent.html", {"email": email})
    return render(request, "accounts/login.html", {"form": form})


@require_http_methods(["GET", "POST"])
def magic_link(request):
    """
    GET vérifie le lien sans le consommer et affiche un bouton de confirmation :
    les scanners de liens des messageries ne peuvent ainsi pas « utiliser » le lien.
    POST consomme le lien (la connexion met à jour last_login, ce qui l'invalide).
    """
    token = request.POST.get("sesame") if request.method == "POST" else request.GET.get("sesame")
    user = get_user(token, update_last_login=False) if token else None
    if user is None:
        return render(request, "accounts/link_invalid.html", status=400)
    if request.method == "GET":
        return render(request, "accounts/magic_link_confirm.html", {"token": token})
    login(request, user)
    if not user.is_profile_complete:
        return redirect("accounts:profile")
    return redirect("items:catalog")


@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    user = request.user
    onboarding = not user.is_profile_complete
    form = ProfileForm(request.POST or None, instance=user)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        if form.cleaned_data.get("accept_terms") and not user.terms_accepted_at:
            user.terms_accepted_at = timezone.now()
        user.save()
        if onboarding:
            messages.success(request, "Bienvenue sur Kerentheque ! Votre profil est prêt.")
            return redirect("items:catalog")
        messages.success(request, "Votre profil a été mis à jour.")
        return redirect("accounts:profile")
    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "onboarding": onboarding,
            "no_neighborhood": not form.fields["neighborhood"].queryset.exists(),
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def delete_account_view(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        delete_account(user)
        messages.success(request, "Votre compte a été supprimé.")
        return redirect("items:catalog")
    return render(request, "accounts/delete_account.html")
