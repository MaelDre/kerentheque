from django.db import transaction
from django.utils import timezone

from contacts.models import ContactRequest
from contacts.services import cancel_pending_for_user


def delete_account(user):
    """Anonymise le compte : l'historique des autres utilisateurs affiche « Utilisateur supprimé »."""
    with transaction.atomic():
        now = timezone.now()
        cancel_pending_for_user(user)
        user.items.filter(deleted_at__isnull=True).update(deleted_at=now)
        # Free-text fields may contain personal data. Item names are kept so other
        # members' history stays readable; report reasons are kept for moderation.
        for item in user.items.exclude(description=""):
            item.description = ""
            item.save(update_fields=["description"])  # save() also refreshes search_text
        ContactRequest.objects.filter(requester=user).update(requester_email="", requester_phone="", message="")
        ContactRequest.objects.filter(item__owner=user).update(owner_email="", owner_phone="")

        user.email = f"deleted-{user.pk}@invalid"
        user.pseudo = None
        user.phone = ""
        user.share_email = False
        user.share_phone = False
        user.neighborhood = None
        user.is_active = False
        user.is_staff = False
        user.is_superuser = False
        user.deleted_at = now
        user.set_unusable_password()
        user.save()
