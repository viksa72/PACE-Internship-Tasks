from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lesson, Course


@receiver(post_save, sender=Lesson)
def on_lesson_created(sender, instance, created, **kwargs):
    if created:
        from apps.notifications.utils import notify_students_new_lesson
        notify_students_new_lesson(instance)


@receiver(post_save, sender=Course)
def on_course_published(sender, instance, created, **kwargs):
    """Notify previous students when a teacher publishes a new course."""
    if instance.is_published:
        # Only fire when the course transitions to published (not on every save)
        try:
            old = Course.objects.get(pk=instance.pk)
        except Course.DoesNotExist:
            return
        from apps.notifications.utils import notify_students_new_course
        notify_students_new_course(instance)
