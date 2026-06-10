from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    """Allow access only to users with the Teacher role."""
    message = 'Only teachers can perform this action.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_teacher)


class IsStudent(BasePermission):
    """Allow access only to users with the Student role."""
    message = 'Only students can perform this action.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_student)


class IsTeacherOwner(BasePermission):
    """Allow access only to the teacher who owns the course."""
    message = 'You do not have permission to modify this course.'

    def has_object_permission(self, request, view, obj):
        # obj can be a Course, Topic, or Lesson
        if hasattr(obj, 'teacher'):
            return obj.teacher == request.user
        if hasattr(obj, 'course'):
            return obj.course.teacher == request.user
        if hasattr(obj, 'topic'):
            return obj.topic.course.teacher == request.user
        return False


class IsEnrolledStudent(BasePermission):
    """Allow access to lesson content only for enrolled students or the course teacher."""
    message = 'You must be enrolled in this course to access lessons.'

    def has_object_permission(self, request, view, obj):
        from apps.courses.models import Enrollment
        user = request.user
        # Get the course from the lesson's topic
        course = obj.topic.course
        if user == course.teacher:
            return True
        return Enrollment.objects.filter(
            student=user, course=course, payment_status='completed'
        ).exists()
