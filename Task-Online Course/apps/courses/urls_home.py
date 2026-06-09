"""Home URL — maps root / to the course catalog."""
from django.urls import path
from apps.courses.views import catalog

urlpatterns = [
    path('', catalog, name='home'),
]
