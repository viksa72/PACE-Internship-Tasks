from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


def create_notification(recipient, title, message, notification_type='general', link=''):
    """Create an in-app notification and send an email."""
    Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notification_type,
        link=link,
    )
    # Send email notification
    try:
        send_mail(
            subject=f'LearnHub — {title}',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            fail_silently=True,
        )
    except Exception:
        pass


def notify_students_new_lesson(lesson):
    """Notify all students enrolled in a course when a new lesson is added."""
    from apps.courses.models import Enrollment
    course = lesson.topic.course
    enrollments = Enrollment.objects.filter(
        course=course, payment_status='completed'
    ).select_related('student')

    link = f'/courses/{course.slug}/'
    for enrollment in enrollments:
        create_notification(
            recipient=enrollment.student,
            title=f'New lesson in "{course.title}"',
            message=(
                f'Hi {enrollment.student.first_name or enrollment.student.username},\n\n'
                f'A new lesson "{lesson.title}" has been added to the course '
                f'"{course.title}" under the topic "{lesson.topic.title}".\n\n'
                f'Login to LearnHub to view it: http://127.0.0.1:8000{link}'
            ),
            notification_type='new_lesson',
            link=link,
        )


def notify_students_new_course(course):
    """Notify students who have enrolled in any previous course by this teacher."""
    from apps.courses.models import Enrollment
    teacher = course.teacher
    # Find students who have purchased other courses by the same teacher
    previous_enrollments = Enrollment.objects.filter(
        course__teacher=teacher,
        payment_status='completed',
    ).exclude(course=course).select_related('student')

    seen_students = set()
    link = f'/courses/{course.slug}/'
    for enrollment in previous_enrollments:
        if enrollment.student_id in seen_students:
            continue
        seen_students.add(enrollment.student_id)
        
        create_notification(
            recipient=enrollment.student,
            title=f'New course by {teacher.get_full_name() or teacher.username}',
            message=(
                f'Hi {enrollment.student.first_name or enrollment.student.username},\n\n'
                f'{teacher.get_full_name() or teacher.username}, whose course you enrolled in, '
                f'just published a new course: "{course.title}".\n\n'
                f'Check it out: http://127.0.0.1:8000{link}'
            ),
            notification_type='new_course',
            link=link,
        )
