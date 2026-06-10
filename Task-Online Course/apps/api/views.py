import random
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import OTPToken
from apps.courses.models import Category, Course, Topic, Lesson, Enrollment
from apps.notifications.models import Notification
from apps.notifications.utils import create_notification

from .serializers import (
    StudentRegisterSerializer, TeacherRegisterSerializer,
    LoginSerializer, OTPVerifySerializer,
    UserMeSerializer, UserMeUpdateSerializer,
    CategorySerializer,
    CourseListSerializer, CourseDetailSerializer, CourseWriteSerializer,
    TopicSerializer, TopicWriteSerializer,
    LessonSerializer, LessonListSerializer,
    EnrollmentSerializer,
    TeacherCourseStatsSerializer, EnrolledStudentSerializer,
    NotificationSerializer,
)
from .permissions import IsTeacher, IsStudent, IsTeacherOwner, IsEnrolledStudent

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# ─── Auth ─────────────────────────────────────────────────────────────────────

class StudentRegisterView(generics.CreateAPIView):
    """POST /api/auth/register/student/ — Register a new student account."""
    serializer_class = StudentRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'message': 'Student account created. Please log in to receive your OTP.',
             'user': {'id': user.id, 'email': user.email, 'username': user.username}},
            status=status.HTTP_201_CREATED
        )


class TeacherRegisterView(generics.CreateAPIView):
    """POST /api/auth/register/teacher/ — Register a new teacher account."""
    serializer_class = TeacherRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'message': 'Teacher account created. Please log in to receive your OTP.',
             'user': {'id': user.id, 'email': user.email, 'username': user.username}},
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    """
    POST /api/auth/login/
    Authenticates credentials and sends a 6-digit OTP to the user's email.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate and store OTP
        otp_code = str(random.randint(100000, 999999))
        OTPToken.objects.filter(user=user, is_used=False).update(is_used=True)
        OTPToken.objects.create(user=user, token=otp_code)

        # Send the OTP email
        create_notification(
            recipient=user,
            title='Your LearnHub OTP Code',
            message=(
                f'Hi {user.first_name or user.username},\n\n'
                f'Your one-time login code is: {otp_code}\n\n'
                f'This code expires in 10 minutes. Do not share it with anyone.'
            ),
            notification_type='general',
        )

        return Response(
            {'message': f'OTP sent to {email}. Please check your email.',
             'email': email},
            status=status.HTTP_200_OK
        )


class OTPVerifyView(APIView):
    """
    POST /api/auth/verify-otp/
    Submits the 6-digit OTP and returns JWT access + refresh tokens on success.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        token_obj = OTPToken.objects.filter(
            user=user, token=otp_code, is_used=False
        ).order_by('-created_at').first()

        if not token_obj or not token_obj.is_valid():
            return Response(
                {'error': 'Invalid or expired OTP. Please request a new one.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token_obj.is_used = True
        token_obj.save()

        tokens = get_tokens_for_user(user)
        return Response(
            {'message': 'Login successful.',
             'tokens': tokens,
             'user': {
                 'id': user.id,
                 'email': user.email,
                 'username': user.username,
                 'role': user.role,
             }},
            status=status.HTTP_200_OK
        )


class MeView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/auth/me/ — Return the current authenticated user's profile.
    PATCH /api/auth/me/ — Update name / bio / expertise fields.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserMeUpdateSerializer
        return UserMeSerializer

    def get_object(self):
        return self.request.user


# ─── Categories ───────────────────────────────────────────────────────────────

class CategoryListView(generics.ListAPIView):
    """GET /api/categories/ — List all course categories (public)."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


# ─── Courses ──────────────────────────────────────────────────────────────────

class CourseListView(generics.ListAPIView):
    """
    GET /api/courses/ — List all published courses (public).
    Supports ?search=, ?category=slug, ?level=, ?ordering=
    """
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'short_description', 'teacher__username',
                     'teacher__first_name', 'teacher__last_name']
    ordering_fields = ['price', 'created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Course.objects.filter(is_published=True).select_related('category', 'teacher')
        category_slug = self.request.query_params.get('category')
        level = self.request.query_params.get('level')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if level:
            qs = qs.filter(level=level)
        return qs


class CourseCreateView(generics.CreateAPIView):
    """POST /api/courses/ — Create a new course. Teacher only."""
    serializer_class = CourseWriteSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = serializer.save(teacher=request.user)
        return Response(
            CourseDetailSerializer(course, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/courses/{slug}/ — Course detail (public).
    PATCH  /api/courses/{slug}/ — Update course (Teacher owner only).
    DELETE /api/courses/{slug}/ — Delete course (Teacher owner only).
    """
    lookup_field = 'slug'
    queryset = Course.objects.select_related('category', 'teacher').prefetch_related('topics__lessons')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsTeacher(), IsTeacherOwner()]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return CourseWriteSerializer
        return CourseDetailSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = CourseWriteSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        course = serializer.save()
        return Response(CourseDetailSerializer(course, context={'request': request}).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({'message': 'Course deleted.'}, status=status.HTTP_204_NO_CONTENT)


# ─── Topics ───────────────────────────────────────────────────────────────────

class TopicListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/courses/{slug}/topics/ — List topics (public).
    POST /api/courses/{slug}/topics/ — Add a topic (Teacher owner only).
    """
    def get_course(self):
        return get_object_or_404(Course, slug=self.kwargs['slug'])

    def get_queryset(self):
        return Topic.objects.filter(course__slug=self.kwargs['slug']).prefetch_related('lessons')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsTeacher()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TopicWriteSerializer
        return TopicSerializer

    def perform_create(self, serializer):
        course = self.get_course()
        if course.teacher != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You do not own this course.')
        serializer.save(course=course)

    def create(self, request, *args, **kwargs):
        serializer = TopicWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = self.get_course()
        if course.teacher != request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You do not own this course.')
        topic = serializer.save(course=course)
        return Response(TopicSerializer(topic).data, status=status.HTTP_201_CREATED)


class TopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/courses/{slug}/topics/{id}/ — Topic detail.
    PATCH  /api/courses/{slug}/topics/{id}/ — Update topic (Teacher owner only).
    DELETE /api/courses/{slug}/topics/{id}/ — Delete topic (Teacher owner only).
    """
    def get_queryset(self):
        return Topic.objects.filter(course__slug=self.kwargs['slug'])

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsTeacher()]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return TopicWriteSerializer
        return TopicSerializer

    def check_ownership(self, topic):
        if topic.course.teacher != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You do not own this course.')

    def update(self, request, *args, **kwargs):
        topic = self.get_object()
        self.check_ownership(topic)
        serializer = TopicWriteSerializer(topic, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        topic = serializer.save()
        return Response(TopicSerializer(topic).data)

    def destroy(self, request, *args, **kwargs):
        topic = self.get_object()
        self.check_ownership(topic)
        topic.delete()
        return Response({'message': 'Topic deleted.'}, status=status.HTTP_204_NO_CONTENT)


# ─── Lessons ──────────────────────────────────────────────────────────────────

class LessonListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/courses/{slug}/topics/{topic_id}/lessons/ — List lessons.
    POST /api/courses/{slug}/topics/{topic_id}/lessons/ — Add lesson (Teacher owner only).
    """
    def get_topic(self):
        return get_object_or_404(
            Topic, pk=self.kwargs['topic_id'], course__slug=self.kwargs['slug']
        )

    def get_queryset(self):
        return Lesson.objects.filter(
            topic_id=self.kwargs['topic_id'],
            topic__course__slug=self.kwargs['slug']
        )

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsTeacher()]

    def get_serializer_class(self):
        return LessonSerializer

    def list(self, request, *args, **kwargs):
        topic = self.get_topic()
        course = topic.course
        user = request.user
        # Only teacher or enrolled student can see full lesson content
        is_owner = (user == course.teacher)
        is_enrolled = Enrollment.objects.filter(
            student=user, course=course, payment_status='completed'
        ).exists()

        if not is_owner and not is_enrolled:
            # Return restricted listing (no content, no video)
            lessons = self.get_queryset()
            serializer = LessonListSerializer(lessons, many=True)
            return Response({
                'detail': 'Enroll to access full lesson content.',
                'lessons': serializer.data
            })

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        topic = self.get_topic()
        if topic.course.teacher != request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You do not own this course.')
        serializer = LessonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lesson = serializer.save(topic=topic)
        return Response(LessonSerializer(lesson).data, status=status.HTTP_201_CREATED)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/courses/{slug}/topics/{topic_id}/lessons/{id}/ — Lesson detail.
    PATCH  /api/courses/{slug}/topics/{topic_id}/lessons/{id}/ — Update (Teacher owner).
    DELETE /api/courses/{slug}/topics/{topic_id}/lessons/{id}/ — Delete (Teacher owner).
    """
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(
            topic_id=self.kwargs['topic_id'],
            topic__course__slug=self.kwargs['slug']
        )

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsTeacher()]

    def check_ownership(self, lesson):
        if lesson.topic.course.teacher != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You do not own this course.')

    def retrieve(self, request, *args, **kwargs):
        lesson = self.get_object()
        course = lesson.topic.course
        user = request.user
        is_owner = (user == course.teacher)
        is_enrolled = Enrollment.objects.filter(
            student=user, course=course, payment_status='completed'
        ).exists()
        if not is_owner and not is_enrolled:
            return Response(
                {'detail': 'You must be enrolled to view this lesson.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return Response(LessonSerializer(lesson).data)

    def update(self, request, *args, **kwargs):
        lesson = self.get_object()
        self.check_ownership(lesson)
        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        lesson = serializer.save()
        return Response(LessonSerializer(lesson).data)

    def destroy(self, request, *args, **kwargs):
        lesson = self.get_object()
        self.check_ownership(lesson)
        lesson.delete()
        return Response({'message': 'Lesson deleted.'}, status=status.HTTP_204_NO_CONTENT)


# ─── Enrollments ──────────────────────────────────────────────────────────────

class EnrollmentListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/enrollments/ — List current student's enrollments.
    POST /api/enrollments/ — Enroll in a course (Student only).
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Enrollment.objects.filter(
            student=self.request.user
        ).select_related('course__category', 'course__teacher')


# ─── Teacher Dashboard ────────────────────────────────────────────────────────

class TeacherCoursesView(generics.ListAPIView):
    """GET /api/teacher/courses/ — List teacher's own courses with stats."""
    serializer_class = TeacherCourseStatsSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)


class TeacherCourseStudentsView(generics.ListAPIView):
    """GET /api/teacher/courses/{slug}/students/ — Enrolled students for a course."""
    serializer_class = EnrolledStudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        course = get_object_or_404(
            Course, slug=self.kwargs['slug'], teacher=self.request.user
        )
        return Enrollment.objects.filter(
            course=course, payment_status='completed'
        ).select_related('student')


# ─── Notifications ────────────────────────────────────────────────────────────

class NotificationListView(generics.ListAPIView):
    """GET /api/notifications/ — List current user's notifications."""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('-created_at')


class MarkNotificationReadView(APIView):
    """POST /api/notifications/{id}/read/ — Mark a single notification as read."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
        notif.is_read = True
        notif.save()
        return Response({'message': 'Notification marked as read.'}, status=status.HTTP_200_OK)


class MarkAllNotificationsReadView(APIView):
    """POST /api/notifications/read-all/ — Mark all notifications as read."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({'message': 'All notifications marked as read.'}, status=status.HTTP_200_OK)
