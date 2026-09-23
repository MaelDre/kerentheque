from django.conf import settings
from django.db import models
from django.urls import reverse

from .search import normalize


class Category(models.Model):
    name = models.CharField("nom", max_length=100, unique=True)
    position = models.PositiveIntegerField("ordre d'affichage", default=0)
    is_active = models.BooleanField("active", default=True)

    class Meta:
        ordering = ["position", "name"]
        verbose_name = "catégorie"
        verbose_name_plural = "catégories"

    def __str__(self):
        return self.name


class ItemQuerySet(models.QuerySet):
    def not_deleted(self):
        return self.filter(deleted_at__isnull=True)

    def available(self):
        """Objets visibles dans le catalogue : non supprimés, propriétaire actif."""
        return self.not_deleted().filter(owner__is_active=True)


class Item(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="propriétaire", on_delete=models.CASCADE, related_name="items"
    )
    name = models.CharField("nom", max_length=100)
    category = models.ForeignKey(Category, verbose_name="catégorie", on_delete=models.PROTECT)
    description = models.TextField("description", max_length=2000, blank=True)
    created_at = models.DateTimeField("ajouté le", auto_now_add=True)
    deleted_at = models.DateTimeField("supprimé le", null=True, blank=True)
    search_text = models.TextField(editable=False, default="")

    objects = ItemQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = "objet"
        verbose_name_plural = "objets"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.search_text = normalize(f"{self.name} {self.description}")
        if kwargs.get("update_fields") is not None and {"name", "description"} & set(kwargs["update_fields"]):
            kwargs["update_fields"] = {*kwargs["update_fields"], "search_text"}
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("items:detail", args=[self.pk])

    @property
    def is_available(self):
        return self.deleted_at is None and self.owner.is_active
