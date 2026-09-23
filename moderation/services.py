from django.db import transaction

from contacts.services import cancel_pending_for_user


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
