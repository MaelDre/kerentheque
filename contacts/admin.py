from django.contrib import admin

from .models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    """Consultation seule : les statuts ne changent que par les actions des membres ou la modération."""

    list_display = ["item_name", "requester", "status", "created_at", "decided_at"]
    list_filter = ["status"]
    search_fields = ["item_name", "requester__pseudo", "requester__email"]
    list_select_related = ["requester"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
