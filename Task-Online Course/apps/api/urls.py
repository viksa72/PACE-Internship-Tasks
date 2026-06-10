from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    # Auth
    StudentRegisterView, TeacherRegisterView,
    LoginView, OTPVerifyView, MeView,
    # Categories
    CategoryListView,
    # Courses
    CourseListView, CourseCreateView, CourseDetailView,
    # Topics
    TopicListCreateView, TopicDetailView,
    # Lessons
    LessonListCreateView, LessonDetailView,
    # Enrollments
    EnrollmentListCreateView,
    # Teacher Dashboard
    TeacherCoursesView, TeacherCourseStudentsView,
    # Notifications
    NotificationListView, MarkNotificationReadView, MarkAllNotificationsReadView,
)

app_name = 'api'

urlpatterns = [
    # ── Auth ──────────────────────────────────────────────────────────────────
    path('auth/register/student/', StudentRegisterView.as_view(), name='student-register'),
    path('auth/register/teacher/', TeacherRegisterView.as_view(), name='teacher-register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/me/', MeView.as_view(), name='me'),

    # ── Categories ────────────────────────────────────────────────────────────
    path('categories/', CategoryListView.as_view(), name='category-list'),

    # ── Courses ───────────────────────────────────────────────────────────────
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course-detail'),

    # ── Topics ────────────────────────────────────────────────────────────────
    path('courses/<slug:slug>/topics/', TopicListCreateView.as_view(), name='topic-list-create'),
    path('courses/<slug:slug>/topics/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),

    # ── Lessons ───────────────────────────────────────────────────────────────
    path('courses/<slug:slug>/topics/<int:topic_id>/lessons/',
         LessonListCreateView.as_view(), name='lesson-list-create'),
    path('courses/<slug:slug>/topics/<int:topic_id>/lessons/<int:pk>/',
         LessonDetailView.as_view(), name='lesson-detail'),

    # ── Enrollments ───────────────────────────────────────────────────────────
    path('enrollments/', EnrollmentListCreateView.as_view(), name='enrollment-list-create'),

    # ── Teacher Dashboard ─────────────────────────────────────────────────────
    path('teacher/courses/', TeacherCoursesView.as_view(), name='teacher-courses'),
    path('teacher/courses/<slug:slug>/students/',
         TeacherCourseStudentsView.as_view(), name='teacher-course-students'),

    # ── Notifications ─────────────────────────────────────────────────────────
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/read-all/', MarkAllNotificationsReadView.as_view(), name='notifications-read-all'),
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-read'),
]
