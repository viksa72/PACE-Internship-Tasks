from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search-ajax/', views.search_ajax, name='search_ajax'),
    
    # Employee URLs
    path('employee/add/', views.add_employee, name='add_employee'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employee/<int:pk>/edit/', views.edit_employee, name='edit_employee'),
    path('employee/<int:pk>/delete/', views.delete_employee, name='delete_employee'),
    path('employee/<int:pk>/pdf/', views.generate_resume_pdf, name='generate_resume_pdf'),
    
    # Project URLs
    path('projects/', views.list_projects, name='list_projects'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:pk>/delete/', views.delete_project, name='delete_project'),
    
    # Mapping URLs
    path('employee/<int:employee_pk>/map/', views.add_mapping, name='add_mapping'),
    path('mapping/<int:pk>/edit/', views.edit_mapping, name='edit_mapping'),
    path('mapping/<int:pk>/delete/', views.delete_mapping, name='delete_mapping'),
]
