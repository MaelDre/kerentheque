from django.contrib import admin, messages

from .models import Category, Item
from .services import delete_item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "position", "is_active"]
    list_editable = ["position", "is_active"]
    search_fields = ["name"]


class DeletedFilter(admin.SimpleListFilter):
    title = "supprimé"
    parameter_name = "deleted"

    def lookups(self, request, model_admin):
        return [("no", "Non"), ("yes", "Oui")]

    def queryset(self, request, queryset):
        if self.value() == "no":
            return queryset.filter(deleted_at__isnull=True)
        if self.value() == "yes":
            return queryset.filter(deleted_at__isnull=False)
        return queryset


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "category", "created_at", "deleted_at"]
    list_filter = [DeletedFilter, "category"]
    search_fields = ["name", "description", "owner__pseudo", "owner__email"]
    list_select_related = ["owner", "category"]
    readonly_fields = ["owner", "created_at", "deleted_at"]
    actions = ["remove_items"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False  # le retrait passe par l'action, qui annule les demandes en attente

    @admin.action(description="Retirer du catalogue les objets sélectionnés")
    def remove_items(self, request, queryset):
        for item in queryset.filter(deleted_at__isnull=True):
            delete_item(item)
        self.message_user(request, "Objets retirés du catalogue.", messages.SUCCESS)
