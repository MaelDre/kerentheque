from django.conf import settings
from django.db import models


class Report(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="auteur", on_delete=models.CASCADE, related_name="reports_sent"
    )
    item = models.ForeignKey(
        "items.Item", verbose_name="objet signalé", on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="utilisateur signalé",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports_received",
    )
    reason = models.TextField("motif", max_length=1000)
    created_at = models.DateTimeField("signalé le", auto_now_add=True)
    handled_at = models.DateTimeField("traité le", null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = "signalement"
        verbose_name_plural = "signalements"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(item__isnull=False) | models.Q(user__isnull=False), name="report_has_target"
            ),
        ]

    def __str__(self):
        return f"Signalement de {self.target_label}"

    @property
    def target_label(self):
        return f"l'objet « {self.item} »" if self.item_id else f"l'utilisateur {self.user}"
