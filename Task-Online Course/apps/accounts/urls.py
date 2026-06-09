from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/teacher/', views.teacher_signup, name='teacher_signup'),
    path('login/', views.user_login, name='login'),
    path('otp/verify/', views.otp_verify, name='otp_verify'),
    path('otp/resend/', views.resend_otp, name='resend_otp'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
