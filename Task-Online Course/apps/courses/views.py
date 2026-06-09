from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Course, Category, Topic, Lesson, Enrollment
from .forms import CourseForm, TopicForm, LessonForm


def catalog(request):
    """Public course catalog with search and category filter."""
    courses = Course.objects.filter(is_published=True).select_related('teacher', 'category')
    categories = Category.objects.all()

    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    level = request.GET.get('level', '')
    sort = request.GET.get('sort', '-created_at')

    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(teacher__first_name__icontains=query) |
            Q(teacher__last_name__icontains=query)
        )
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    if level:
        courses = courses.filter(level=level)

    sort_options = {
        '-created_at': '-created_at',
        'price_asc': 'price',
        'price_desc': '-price',
        'title': 'title',
    }
    courses = courses.order_by(sort_options.get(sort, '-created_at'))

    # Get enrolled course IDs for the logged-in student
    enrolled_ids = []
    if request.user.is_authenticated and request.user.is_student:
        enrolled_ids = list(
            Enrollment.objects.filter(
                student=request.user, payment_status='completed'
            ).values_list('course_id', flat=True)
        )

    return render(request, 'courses/catalog.html', {
        'courses': courses,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
        'selected_level': level,
        'selected_sort': sort,
        'enrolled_ids': enrolled_ids,
    })


def course_detail(request, slug):
    """Course detail/landing page."""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    topics = course.topics.prefetch_related('lessons').all()
    is_enrolled = False

    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            student=request.user, course=course, payment_status='completed'
        ).exists()

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'topics': topics,
        'is_enrolled': is_enrolled,
    })


@login_required
def lesson_view(request, course_slug, lesson_id):
    """View a lesson — only for enrolled students or the course teacher."""
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, pk=lesson_id, topic__course=course)

    is_teacher = request.user == course.teacher
    is_enrolled = Enrollment.objects.filter(
        student=request.user, course=course, payment_status='completed'
    ).exists()

    if not is_teacher and not is_enrolled:
        messages.error(request, 'You must enroll in this course to view lessons.')
        return redirect('courses:course_detail', slug=course_slug)

    topics = course.topics.prefetch_related('lessons').all()
    return render(request, 'courses/lesson_view.html', {
        'course': course,
        'lesson': lesson,
        'topics': topics,
    })


# ─── Teacher Views ────────────────────────────────────────────────────────────

def teacher_required(view_func):
    """Decorator: ensure user is authenticated and is a teacher."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_teacher:
            messages.error(request, 'Access denied. Teacher accounts only.')
            return redirect('courses:catalog')
        return view_func(request, *args, **kwargs)
    return wrapper


@teacher_required
def teacher_dashboard(request):
    """Teacher's main dashboard showing all their courses."""
    courses = Course.objects.filter(teacher=request.user).order_by('-created_at')
    total_students = sum(c.enrollment_count for c in courses)
    return render(request, 'courses/teacher_dashboard.html', {
        'courses': courses,
        'total_students': total_students,
    })


@teacher_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, f'Course "{course.title}" created successfully!')
            return redirect('courses:course_manage', slug=course.slug)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Create'})


@teacher_required
def course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug, teacher=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('courses:course_manage', slug=course.slug)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {
        'form': form, 'course': course, 'action': 'Edit'
    })


@teacher_required
def course_delete(request, slug):
    course = get_object_or_404(Course, slug=slug, teacher=request.user)
    if request.method == 'POST':
        title = course.title
        course.delete()
        messages.success(request, f'Course "{title}" deleted.')
        return redirect('courses:teacher_dashboard')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


@teacher_required
def course_manage(request, slug):
    """Teacher's course management page — topics and lessons."""
    course = get_object_or_404(Course, slug=slug, teacher=request.user)
    topics = course.topics.prefetch_related('lessons').all()
    return render(request, 'courses/course_manage.html', {
        'course': course, 'topics': topics
    })


@teacher_required
def topic_create(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, teacher=request.user)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.course = course
            topic.save()
            messages.success(request, f'Topic "{topic.title}" added.')
            return redirect('courses:course_manage', slug=course_slug)
    else:
        form = TopicForm()
    return render(request, 'courses/topic_form.html', {
        'form': form, 'course': course, 'action': 'Add'
    })


@teacher_required
def topic_edit(request, course_slug, topic_id):
    course = get_object_or_404(Course, slug=course_slug, teacher=request.user)
    topic = get_object_or_404(Topic, pk=topic_id, course=course)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Topic updated.')
            return redirect('courses:course_manage', slug=course_slug)
    else:
        form = TopicForm(instance=topic)
    return render(request, 'courses/topic_form.html', {
        'form': form, 'course': course, 'topic': topic, 'action': 'Edit'
    })


@teacher_required
def topic_delete(request, course_slug, topic_id):
    course = get_object_or_404(Course, slug=course_slug, teacher=request.user)
    topic = get_object_or_404(Topic, pk=topic_id, course=course)
    if request.method == 'POST':
        topic.delete()
        messages.success(request, 'Topic deleted.')
        return redirect('courses:course_manage', slug=course_slug)
    return render(request, 'courses/topic_confirm_delete.html', {
        'topic': topic, 'course': course
    })


@teacher_required
def lesson_create(request, course_slug, topic_id):
    course = get_object_or_404(Course, slug=course_slug, teacher=request.user)
    topic = get_object_or_404(Topic, pk=topic_id, course=course)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.topic = topic
            lesson.save()
            messages.success(request, f'Lesson "{lesson.title}" added.')
            return redirect('courses:course_manage', slug=course_slug)
    else:
        form = LessonForm()
    return render(request, 'courses/lesson_form.html', {
        'form': form, 'course': course, 'topic': topic, 'action': 'Add'
    })


@teacher_required
def lesson_edit(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, teacher=request.user)
    lesson = get_object_or_404(Lesson, pk=lesson_id, topic__course=course)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lesson updated.')
            return redirect('courses:course_manage', slug=course_slug)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'courses/lesson_form.html', {
        'form': form, 'course': course, 'lesson': lesson,
        'topic': lesson.topic, 'action': 'Edit'
    })


@teacher_required
def lesson_delete(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, teacher=request.user)
    lesson = get_object_or_404(Lesson, pk=lesson_id, topic__course=course)
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, 'Lesson deleted.')
        return redirect('courses:course_manage', slug=course_slug)
    return render(request, 'courses/lesson_confirm_delete.html', {
        'lesson': lesson, 'course': course
    })


@teacher_required
def enrolled_students(request, slug):
    """View all students enrolled in a course."""
    course = get_object_or_404(Course, slug=slug, teacher=request.user)
    enrollments = Enrollment.objects.filter(
        course=course, payment_status='completed'
    ).select_related('student').order_by('-enrolled_at')
    return render(request, 'courses/enrolled_students.html', {
        'course': course, 'enrollments': enrollments
    })


@login_required
def my_courses(request):
    """Student's enrolled courses."""
    if not request.user.is_student:
        return redirect('courses:teacher_dashboard')
    enrollments = Enrollment.objects.filter(
        student=request.user, payment_status='completed'
    ).select_related('course', 'course__teacher').order_by('-enrolled_at')
    return render(request, 'courses/my_courses.html', {'enrollments': enrollments})
