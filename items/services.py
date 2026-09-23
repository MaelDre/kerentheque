from django.db import transaction
from django.utils import timezone

from contacts.services import cancel_pending_for_item


def delete_item(item):
    """Suppression logique d'un objet, par son propriétaire ou par la modération."""
    with transaction.atomic():
        if item.deleted_at is None:
            item.deleted_at = timezone.now()
            item.save(update_fields=["deleted_at"])
        cancel_pending_for_item(item)
