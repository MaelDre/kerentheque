from django import template

from moderation.services import platform_stats

register = template.Library()


@register.inclusion_tag("moderation/admin_dashboard.html", takes_context=True)
def admin_dashboard(context):
    """Platform indicators, rendered for superusers only (no query runs otherwise)."""
    request = context.get("request")
    if request is None or not request.user.is_superuser:
        return {"stats": None}
    stats = platform_stats()
    return {
        "stats": [
            (stats["items"], "Objets"),
            (stats["members"], "Membres inscrits"),
            (stats["requests"], "Demandes de prêt"),
            (stats["accepted_requests"], "Mises en relation acceptées"),
        ]
    }
