"""
LearnHub URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('courses/', include('apps.courses.urls', namespace='courses')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
    path('', include('apps.courses.urls_home')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
