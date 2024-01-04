from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rest-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
    path("students/", include("students.urls")),
    path("campuses/", include("campuses.urls")),
    path("libraries/", include("libraries.urls")),
    path("cafe/", include("cafe.urls")),
    path("", include("staffs.urls")),
    # path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
