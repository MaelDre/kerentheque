from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import Report


class HandledFilter(admin.SimpleListFilter):
    title = "traité"
    parameter_name = "handled"

    def lookups(self, request, model_admin):
        return [("no", "Non traités"), ("yes", "Traités")]

    def queryset(self, request, queryset):
        if self.value() == "no":
            return queryset.filter(handled_at__isnull=True)
        if self.value() == "yes":
            return queryset.filter(handled_at__isnull=False)
        return queryset


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["created_at", "target_link", "author", "short_reason", "handled_at"]
    list_filter = [HandledFilter]
    list_select_related = ["author", "item", "user"]
    fields = ["author", "target_link", "reason", "created_at", "handled_at"]
    readonly_fields = fields
    actions = ["mark_handled"]

    def changelist_view(self, request, extra_context=None):
        # Affiche par défaut les signalements non traités.
        if not request.GET and request.method == "GET":
            return HttpResponseRedirect(request.path + "?handled=no")
        return super().changelist_view(request, extra_context)

    @admin.display(description="cible")
    def target_link(self, obj):
        if obj.item_id:
            url = reverse("admin:items_item_change", args=[obj.item_id])
            return format_html('Objet : <a href="{}">{}</a>', url, obj.item)
        url = reverse("admin:accounts_user_change", args=[obj.user_id])
        return format_html('Utilisateur : <a href="{}">{}</a>', url, obj.user)

    @admin.display(description="motif")
    def short_reason(self, obj):
        return obj.reason if len(obj.reason) <= 80 else obj.reason[:80] + "…"

    def has_add_permission(self, request):
        return False

    @admin.action(description="Marquer comme traités")
    def mark_handled(self, request, queryset):
        count = queryset.filter(handled_at__isnull=True).update(handled_at=timezone.now())
        self.message_user(request, f"{count} signalement(s) marqué(s) comme traité(s).", messages.SUCCESS)
