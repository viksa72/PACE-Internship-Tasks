from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, TeacherProfile, StudentProfile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'teacher':
            TeacherProfile.objects.get_or_create(user=instance)
        else:
            StudentProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == 'teacher':
        if hasattr(instance, 'teacher_profile'):
            instance.teacher_profile.save()
    else:
        if hasattr(instance, 'student_profile'):
            instance.student_profile.save()
