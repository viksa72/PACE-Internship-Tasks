from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Catalog & public views
    path('', views.catalog, name='catalog'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/lesson/<int:lesson_id>/', views.lesson_view, name='lesson_view'),

    # Student
    path('my/courses/', views.my_courses, name='my_courses'),

    # Teacher Dashboard
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/course/create/', views.course_create, name='course_create'),
    path('teacher/course/<slug:slug>/edit/', views.course_edit, name='course_edit'),
    path('teacher/course/<slug:slug>/delete/', views.course_delete, name='course_delete'),
    path('teacher/course/<slug:slug>/manage/', views.course_manage, name='course_manage'),
    path('teacher/course/<slug:slug>/students/', views.enrolled_students, name='enrolled_students'),

    # Topics
    path('teacher/course/<slug:course_slug>/topic/add/', views.topic_create, name='topic_create'),
    path('teacher/course/<slug:course_slug>/topic/<int:topic_id>/edit/', views.topic_edit, name='topic_edit'),
    path('teacher/course/<slug:course_slug>/topic/<int:topic_id>/delete/', views.topic_delete, name='topic_delete'),

    # Lessons
    path('teacher/course/<slug:course_slug>/topic/<int:topic_id>/lesson/add/', views.lesson_create, name='lesson_create'),
    path('teacher/course/<slug:course_slug>/lesson/<int:lesson_id>/edit/', views.lesson_edit, name='lesson_edit'),
    path('teacher/course/<slug:course_slug>/lesson/<int:lesson_id>/delete/', views.lesson_delete, name='lesson_delete'),
]
