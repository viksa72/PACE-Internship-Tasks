from django.contrib.auth.models import AbstractUser
from django.db import models
import pyotp
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    is_otp_verified = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=64, blank=True, default='')

    def save(self, *args, **kwargs):
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()
        super().save(*args, **kwargs)

    @property
    def is_teacher(self):
        return self.role == 'teacher'

    @property
    def is_student(self):
        return self.role == 'student'

    def __str__(self):
        return f"{self.username} ({self.role})"


class OTPToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otp_tokens')
    token = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        expiry = self.created_at + timedelta(minutes=10)
        return not self.is_used and timezone.now() <= expiry

    def __str__(self):
        return f"OTP for {self.user.email}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/teachers/', blank=True, null=True)
    expertise = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"Teacher: {self.user.get_full_name() or self.user.username}"


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    avatar = models.ImageField(upload_to='avatars/students/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Student: {self.user.get_full_name() or self.user.username}"
