import re

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone


class Neighborhood(models.Model):
    """Quartier : localisation approximative publique d'un utilisateur."""

    name = models.CharField("nom", max_length=100, unique=True)
    position = models.PositiveIntegerField("ordre d'affichage", default=0)
    is_active = models.BooleanField("actif", default=True)

    class Meta:
        ordering = ["position", "name"]
        verbose_name = "quartier"
        verbose_name_plural = "quartiers"

    def __str__(self):
        return self.name


def validate_phone(value):
    """Validation souple : chiffres, espaces, points, tirets et « + », entre 10 et 15 chiffres."""
    if not re.fullmatch(r"\+?[\d .\-]+", value) or not 10 <= len(re.sub(r"\D", "", value)) <= 15:
        raise ValidationError("Numéro de téléphone invalide.")


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire.")
        user = self.model(email=self.normalize_email(email).lower(), **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user = self.model(email=self.normalize_email(email).lower(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email", unique=True)
    pseudo = models.CharField("pseudo", max_length=30, null=True, blank=True)
    neighborhood = models.ForeignKey(
        Neighborhood, verbose_name="quartier", on_delete=models.PROTECT, null=True, blank=True
    )
    phone = models.CharField("téléphone", max_length=20, blank=True, validators=[validate_phone])
    share_email = models.BooleanField("partager mon email", default=True)
    share_phone = models.BooleanField("partager mon téléphone", default=False)
    terms_accepted_at = models.DateTimeField("conditions acceptées le", null=True, blank=True)

    is_active = models.BooleanField(
        "actif", default=True, help_text="Décoché : compte suspendu ou supprimé, connexion impossible."
    )
    is_staff = models.BooleanField("administrateur", default=False)
    date_joined = models.DateTimeField("inscrit le", default=timezone.now)
    deleted_at = models.DateTimeField("supprimé le", null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"
        constraints = [
            models.UniqueConstraint(Lower("pseudo"), name="unique_pseudo_ci"),
        ]

    def __str__(self):
        return self.display_name if self.pseudo or self.deleted_at else self.email

    @property
    def display_name(self):
        if self.deleted_at:
            return "Utilisateur supprimé"
        return self.pseudo or "—"

    @property
    def is_profile_complete(self):
        return bool(self.pseudo and self.neighborhood_id and self.terms_accepted_at)

    @property
    def is_suspended(self):
        return not self.is_active and self.deleted_at is None

    def shared_contact(self):
        """Coordonnées que l'utilisateur accepte actuellement de transmettre."""
        return {
            "email": self.email if self.share_email else "",
            "phone": self.phone if self.share_phone and self.phone else "",
        }
