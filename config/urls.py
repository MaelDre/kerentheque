from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Administration Kerentheque"
admin.site.site_title = "Kerentheque"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("compte/", include("accounts.urls")),
    path("", include("contacts.urls")),
    path("", include("moderation.urls")),
    path("", include("items.urls")),
]
