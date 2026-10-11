import logging

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def notify_feedback(user, message):
    body = f"Message de {user.email} :\n\n{message}"
    email = EmailMessage(
        subject="Nouveau message via le formulaire de contact",
        body=body,
        to=[settings.FEEDBACK_RECIPIENT_EMAIL],
        reply_to=[user.email],
    )
    try:
        email.send()
    except Exception:
        # Un échec d'envoi ne doit pas empêcher l'utilisateur de voir une confirmation.
        logger.exception("Échec de l'envoi du message de contact de %s", user.email)
