"""Règles métier des demandes de contact. Les vues et l'admin ne modifient jamais les statuts directement."""

from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils import timezone

from . import emails
from .models import ContactRequest

Status = ContactRequest.Status


class RequestError(Exception):
    """Action refusée ; le message est destiné à l'utilisateur."""


def existing_request(user, item):
    if not user.is_authenticated:
        return None
    return ContactRequest.objects.filter(item=item, requester=user).first()


def send_request(requester, item, message=""):
    with transaction.atomic():
        if item.owner_id == requester.pk:
            raise RequestError("Vous ne pouvez pas faire de demande pour votre propre objet.")
        if not item.is_available:
            raise RequestError("Cet objet n'est plus disponible.")
        if ContactRequest.objects.filter(item=item, requester=requester).exists():
            raise RequestError("Vous avez déjà fait une demande pour cet objet.")
        pending = ContactRequest.objects.filter(requester=requester, status=Status.PENDING).count()
        if pending >= settings.MAX_PENDING_REQUESTS:
            raise RequestError(
                f"Vous avez déjà {pending} demandes en attente. "
                "Attendez une réponse à vos demandes en cours avant d'en envoyer une nouvelle."
            )
        contact = requester.shared_contact()
        try:
            contact_request = ContactRequest.objects.create(
                item=item,
                requester=requester,
                message=message,
                item_name=item.name,
                requester_email=contact["email"],
                requester_phone=contact["phone"],
            )
        except IntegrityError:
            raise RequestError("Vous avez déjà fait une demande pour cet objet.")
        transaction.on_commit(lambda: emails.notify_new_request(contact_request))
    return contact_request


def _decide(contact_request, owner, **fields):
    """Passe une demande en attente à un statut final ; échoue si elle n'est plus en attente."""
    updated = ContactRequest.objects.filter(
        pk=contact_request.pk, status=Status.PENDING, item__owner=owner
    ).update(decided_at=timezone.now(), **fields)
    if not updated:
        raise RequestError("Cette demande a déjà été traitée ou n'est plus disponible.")
    contact_request.refresh_from_db()
    return contact_request


def accept(contact_request, owner):
    with transaction.atomic():
        contact = owner.shared_contact()
        _decide(
            contact_request,
            owner,
            status=Status.ACCEPTED,
            owner_email=contact["email"],
            owner_phone=contact["phone"],
        )
        transaction.on_commit(lambda: emails.notify_accepted(contact_request))
    return contact_request


def refuse(contact_request, owner):
    # Pas de notification au demandeur : le statut est visible dans « Mes demandes ».
    return _decide(contact_request, owner, status=Status.REFUSED)


def cancel_pending_for_item(item):
    """Annule sans notification les demandes en attente sur un objet."""
    return ContactRequest.objects.filter(item=item, status=Status.PENDING).update(
        status=Status.CANCELLED, decided_at=timezone.now()
    )


def cancel_pending_for_user(user):
    """Annule sans notification les demandes en attente envoyées ou reçues par un utilisateur."""
    return ContactRequest.objects.filter(
        Q(requester=user) | Q(item__owner=user), status=Status.PENDING
    ).update(status=Status.CANCELLED, decided_at=timezone.now())
