from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.accounts.models import TeacherProfile, StudentProfile, OTPToken
from apps.courses.models import Category, Course, Topic, Lesson, Enrollment
from apps.notifications.models import Notification

User = get_user_model()


# ─── Auth / User ─────────────────────────────────────────────────────────────

class StudentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label='Confirm Password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(role='student', **validated_data)
        user.set_password(password)
        user.save()
        return user


class TeacherRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label='Confirm Password')
    expertise = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2',
                  'expertise', 'bio']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        expertise = validated_data.pop('expertise', '')
        bio = validated_data.pop('bio', '')
        user = User(role='teacher', **validated_data)
        user.set_password(password)
        user.save()
        # Update teacher profile extras
        profile = user.teacher_profile
        profile.expertise = expertise
        profile.bio = bio
        profile.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['bio', 'avatar', 'expertise', 'website']


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['bio', 'avatar']


class UserMeSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(read_only=True)
    student_profile = StudentProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'role', 'teacher_profile', 'student_profile']
        read_only_fields = ['role', 'email']


class UserMeUpdateSerializer(serializers.ModelSerializer):
    """Allows updating name fields and their respective profile."""
    bio = serializers.CharField(required=False, allow_blank=True, write_only=True)
    expertise = serializers.CharField(required=False, allow_blank=True, write_only=True)
    website = serializers.URLField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'expertise', 'website']

    def update(self, instance, validated_data):
        bio = validated_data.pop('bio', None)
        expertise = validated_data.pop('expertise', None)
        website = validated_data.pop('website', None)

        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update profile fields
        if instance.is_teacher:
            profile = instance.teacher_profile
            if bio is not None:
                profile.bio = bio
            if expertise is not None:
                profile.expertise = expertise
            if website is not None:
                profile.website = website
            profile.save()
        elif instance.is_student:
            profile = instance.student_profile
            if bio is not None:
                profile.bio = bio
            profile.save()

        return instance


# ─── Courses ─────────────────────────────────────────────────────────────────

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url', 'order',
                  'duration_minutes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class LessonListSerializer(serializers.ModelSerializer):
    """Lighter serializer for listing lessons — omits full content for non-enrolled."""
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order', 'duration_minutes', 'video_url']


class TopicSerializer(serializers.ModelSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'title', 'order', 'lesson_count', 'lessons', 'created_at']
        read_only_fields = ['created_at']

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class TopicWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['title', 'order']


class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    teacher_name = serializers.SerializerMethodField()
    enrollment_count = serializers.IntegerField(read_only=True)
    lesson_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'short_description', 'price',
                  'thumbnail', 'level', 'category', 'teacher_name',
                  'enrollment_count', 'lesson_count', 'created_at']

    def get_teacher_name(self, obj):
        return obj.teacher.get_full_name() or obj.teacher.username


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    teacher_name = serializers.SerializerMethodField()
    teacher_id = serializers.IntegerField(source='teacher.id', read_only=True)
    topics = TopicSerializer(many=True, read_only=True)
    enrollment_count = serializers.IntegerField(read_only=True)
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'short_description', 'price',
                  'thumbnail', 'level', 'category', 'teacher_name', 'teacher_id',
                  'topics', 'enrollment_count', 'is_enrolled', 'is_published', 'created_at']

    def get_teacher_name(self, obj):
        return obj.teacher.get_full_name() or obj.teacher.username

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Enrollment.objects.filter(
                student=request.user, course=obj, payment_status='completed'
            ).exists()
        return False


class CourseWriteSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', allow_null=True, required=False
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'short_description', 'price',
                  'thumbnail', 'level', 'category_id', 'is_published']


# ─── Enrollment ───────────────────────────────────────────────────────────────

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.filter(is_published=True),
        source='course', write_only=True
    )

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'course_id', 'enrolled_at', 'payment_status']
        read_only_fields = ['enrolled_at', 'payment_status']

    def validate(self, data):
        student = self.context['request'].user
        course = data['course']
        if Enrollment.objects.filter(
            student=student, course=course, payment_status='completed'
        ).exists():
            raise serializers.ValidationError('You are already enrolled in this course.')
        return data

    def create(self, validated_data):
        student = self.context['request'].user
        enrollment, _ = Enrollment.objects.get_or_create(
            student=student,
            course=validated_data['course'],
            defaults={'payment_status': 'completed'}  # Mock: instant enroll
        )
        if enrollment.payment_status != 'completed':
            enrollment.payment_status = 'completed'
            enrollment.save()
        return enrollment


# ─── Teacher Dashboard ────────────────────────────────────────────────────────

class TeacherCourseStatsSerializer(serializers.ModelSerializer):
    enrollment_count = serializers.IntegerField(read_only=True)
    lesson_count = serializers.IntegerField(read_only=True)
    topic_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'price', 'level', 'is_published',
                  'enrollment_count', 'lesson_count', 'topic_count', 'created_at']


class EnrolledStudentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_email = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = ['id', 'student_name', 'student_email', 'enrolled_at', 'payment_status']

    def get_student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username

    def get_student_email(self, obj):
        return obj.student.email


# ─── Notifications ────────────────────────────────────────────────────────────

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type',
                  'is_read', 'link', 'created_at']
        read_only_fields = ['created_at']
