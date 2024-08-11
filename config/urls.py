from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# API Documentation URLs
api_documentation_patterns = [
    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

# JWT Authentication URLs
jwt_auth_patterns = [
    path(
        "token/",
        include(
            [
                path("refresh/", TokenRefreshView.as_view(), name="refresh_token"),
                path("access/", TokenObtainPairView.as_view(), name="access_token"),
            ]
        ),
    ),
]

# Admin URLs
admin_patterns = [
    path("admin/", admin.site.urls),
]

urlpatterns = [
    path(
        "api/",
        include(
            [
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "schema/ui/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
                path(
                    "schema/redoc/",
                    SpectacularRedocView.as_view(url_name="schema"),
                    name="redoc",
                ),
                path("authentication/", include(jwt_auth_patterns)),
            ]
        ),
    ),
]

achare_api_patterns = [
    path("", include(("achare.authentication.urls", "api"), namespace="authentication")),
]

# Static files (media) settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += achare_api_patterns
# Add admin URLs only if in DEBUG mode
if settings.DEBUG:
    urlpatterns += admin_patterns
