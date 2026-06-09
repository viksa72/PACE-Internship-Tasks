from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create/<int:course_id>/', views.create_payment, name='create'),
    path('execute/', views.execute_payment, name='execute'),
    path('cancel/', views.cancel_payment, name='cancel'),
]
