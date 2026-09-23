from django.shortcuts import redirect
from django.urls import reverse


class ProfileCompletionMiddleware:
    """Redirige vers le formulaire de profil tant qu'un utilisateur connecté ne l'a pas complété."""

    ALLOWED_URL_NAMES = ["accounts:profile", "accounts:logout", "accounts:legal", "accounts:privacy"]
    ALLOWED_PREFIXES = ["/admin/", "/static/"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and not user.is_profile_complete and not self._is_allowed(request.path):
            return redirect("accounts:profile")
        return self.get_response(request)

    def _is_allowed(self, path):
        if any(path.startswith(prefix) for prefix in self.ALLOWED_PREFIXES):
            return True
        return path in {reverse(name) for name in self.ALLOWED_URL_NAMES}
