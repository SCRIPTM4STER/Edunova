from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from .health_views import health_check, health_check_detailed

# API v1 URLs
api_v1_patterns = [
    path('auth/', include('accounts.urls')),
    path('notebook/', include('notebook.urls')),
    path('pdf/', include('PDFs.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Health check endpoints
    path('', health_check, name='health-check'),
    path('api/health/', health_check, name='health-check'),
    path('api/health/detailed/', health_check_detailed, name='health-check-detailed'),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Versioned API routes
    path('api/v1/', include(api_v1_patterns)),
    
    # Legacy routes (backward compatibility)
    path('api/auth/', include('accounts.urls')),
    path('api/notebook/', include('notebook.urls')),
    path('api/pdf/', include('PDFs.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
