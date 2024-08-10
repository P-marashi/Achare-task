"""achare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.contrib.auth.decorators import login_required
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('achare/', include([
        path('Secure/Panel/admin/ui/', admin.site.urls),
        path('Secure/Documentations/ui/', include("docs.urls"))
    ])),
    path('api/', include([
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('schema/ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        path('authentication/token/', include([
            path('refresh/', TokenRefreshView.as_view(), name="refresh_token"),
            path('access/', TokenObtainPairView.as_view(), name="access_token"),
        ])),
    ])),
]
