from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User


class Command(BaseCommand):
    help = "Supprime les comptes créés lors d'une demande de lien mais jamais utilisés pour se connecter."

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=settings.UNUSED_ACCOUNT_RETENTION_DAYS)
        deleted, _ = User.objects.filter(
            last_login__isnull=True, pseudo__isnull=True, is_staff=False, date_joined__lt=cutoff
        ).delete()
        self.stdout.write(f"{deleted} objet(s) supprimé(s).")
