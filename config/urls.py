from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

admin.site.site_header = "Administration Kerentheque"
admin.site.site_title = "Kerentheque"
# Home page adds the platform indicators (superusers only), see moderation/templatetags.
admin.site.index_template = "admin/kerentheque_index.html"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("le-projet/", TemplateView.as_view(template_name="project.html"), name="project"),
    path("compte/", include("accounts.urls")),
    path("", include("contacts.urls")),
    path("", include("moderation.urls")),
    path("", include("feedback.urls")),
    path("", include("items.urls")),
]
