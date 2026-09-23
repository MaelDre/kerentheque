from django.conf import settings
from django.db import models


class ContactRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        ACCEPTED = "accepted", "Acceptée"
        REFUSED = "refused", "Refusée"
        CANCELLED = "cancelled", "Annulée"

    item = models.ForeignKey("items.Item", verbose_name="objet", on_delete=models.CASCADE, related_name="requests")
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="demandeur", on_delete=models.CASCADE, related_name="sent_requests"
    )
    status = models.CharField("statut", max_length=10, choices=Status.choices, default=Status.PENDING)
    message = models.TextField("message", max_length=500, blank=True)

    # Copies figées au moment de la transmission : le nom de l'objet reste lisible
    # après sa suppression, et seules les coordonnées partagées à ce moment-là sont exposées.
    item_name = models.CharField("nom de l'objet", max_length=100)
    requester_email = models.EmailField("email du demandeur", blank=True)
    requester_phone = models.CharField("téléphone du demandeur", max_length=20, blank=True)
    owner_email = models.EmailField("email du propriétaire", blank=True)
    owner_phone = models.CharField("téléphone du propriétaire", max_length=20, blank=True)

    created_at = models.DateTimeField("envoyée le", auto_now_add=True)
    decided_at = models.DateTimeField("traitée le", null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = "demande de contact"
        verbose_name_plural = "demandes de contact"
        constraints = [
            models.UniqueConstraint(fields=["item", "requester"], name="unique_request_per_item"),
        ]

    def __str__(self):
        return f"{self.requester} → {self.item_name} ({self.get_status_display()})"

    @property
    def owner(self):
        return self.item.owner
