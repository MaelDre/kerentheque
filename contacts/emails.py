import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

logger = logging.getLogger(__name__)


def _send(template, subject, recipient, context):
    body = render_to_string(template, {"site_url": settings.SITE_URL, **context})
    try:
        send_mail(subject, body, None, [recipient])
    except Exception:
        # Un échec d'envoi ne doit pas annuler l'action déjà enregistrée.
        logger.exception("Échec de l'envoi de l'email « %s » à %s", subject, recipient)


def notify_new_request(contact_request):
    owner = contact_request.item.owner
    _send(
        "contacts/emails/new_request.txt",
        f"Nouvelle demande pour « {contact_request.item_name} »",
        owner.email,
        {
            "req": contact_request,
            "owner": owner,
            "url": settings.SITE_URL + reverse("contacts:received"),
        },
    )


def notify_accepted(contact_request):
    _send(
        "contacts/emails/accepted.txt",
        f"Demande acceptée pour « {contact_request.item_name} »",
        contact_request.requester.email,
        {
            "req": contact_request,
            "owner": contact_request.item.owner,
            "url": settings.SITE_URL + reverse("contacts:sent"),
        },
    )
