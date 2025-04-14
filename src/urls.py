from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)
from rest_framework.routers import DefaultRouter
from src.events.views import EventViewSet


router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    # Админ-панель
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include(router.urls)),
    path('api/auth/', include('src.custom_auth.urls')),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]