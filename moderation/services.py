from django.contrib.auth import get_user_model
from django.db import transaction

from contacts.models import ContactRequest
from contacts.services import cancel_pending_for_user
from items.models import Item


def suspend_user(user):
    """Bloque la connexion et masque les objets ; les demandes en attente sont annulées."""
    with transaction.atomic():
        user.is_active = False
        user.save(update_fields=["is_active"])
        cancel_pending_for_user(user)


def reactivate_user(user):
    if user.deleted_at is not None:
        return False
    user.is_active = True
    user.save(update_fields=["is_active"])
    return True


def platform_stats():
    """Indicateurs d'activité affichés aux super-administrateurs sur l'accueil de l'admin."""
    User = get_user_model()
    # SQL equivalent of User.is_profile_complete (pseudo, neighborhood, terms accepted):
    # keep both definitions in sync.
    members = (
        User.objects.filter(
            is_active=True,
            deleted_at__isnull=True,
            pseudo__isnull=False,
            neighborhood__isnull=False,
            terms_accepted_at__isnull=False,
        )
        .exclude(pseudo="")
    )
    requests = ContactRequest.objects.all()
    return {
        "items": Item.objects.not_deleted().count(),
        "members": members.count(),
        "requests": requests.count(),
        "accepted_requests": requests.filter(status=ContactRequest.Status.ACCEPTED).count(),
    }
