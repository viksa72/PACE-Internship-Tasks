"""
LearnHub URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Existing HTML views
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('courses/', include('apps.courses.urls', namespace='courses')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
    path('', include('apps.courses.urls_home')),
    # REST API
    path('api/', include('apps.api.urls', namespace='api')),
    # API Docs (Swagger UI)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
