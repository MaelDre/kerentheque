from django.contrib import admin, messages

from moderation.services import reactivate_user, suspend_user

from .models import Neighborhood, User


@admin.register(Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ["name", "position", "is_active"]
    list_editable = ["position", "is_active"]
    search_fields = ["name"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "pseudo", "neighborhood", "status", "date_joined", "is_staff"]
    list_filter = ["is_active", "is_staff", "neighborhood"]
    search_fields = ["email", "pseudo"]
    ordering = ["-date_joined"]
    fields = [
        "email",
        "pseudo",
        "neighborhood",
        "phone",
        "share_email",
        "share_phone",
        "is_active",
        "is_staff",
        "is_superuser",
        "terms_accepted_at",
        "date_joined",
        "last_login",
        "deleted_at",
    ]
    # La suspension passe par les actions pour que les demandes en attente soient annulées.
    readonly_fields = ["is_active", "terms_accepted_at", "date_joined", "last_login", "deleted_at"]
    actions = ["suspend", "reactivate"]

    @admin.display(description="statut")
    def status(self, obj):
        if obj.deleted_at:
            return "Supprimé"
        return "Suspendu" if not obj.is_active else "Actif"

    def has_add_permission(self, request):
        return False  # les comptes se créent par le lien magique (ou `createsuperuser`)

    def has_delete_permission(self, request, obj=None):
        return False  # suppression uniquement par l'utilisateur lui-même (anonymisation)

    @admin.action(description="Suspendre les comptes sélectionnés")
    def suspend(self, request, queryset):
        for user in queryset.filter(is_active=True):
            suspend_user(user)
        self.message_user(request, "Comptes suspendus.", messages.SUCCESS)

    @admin.action(description="Réactiver les comptes sélectionnés")
    def reactivate(self, request, queryset):
        count = sum(reactivate_user(user) for user in queryset.filter(is_active=False))
        self.message_user(request, f"{count} compte(s) réactivé(s).", messages.SUCCESS)
