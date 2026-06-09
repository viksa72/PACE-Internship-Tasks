from django.contrib import admin
from .models import Course, Category, Topic, Lesson, Enrollment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'category', 'price', 'is_published', 'created_at']
    list_filter = ['is_published', 'category', 'level']
    search_fields = ['title', 'teacher__username']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'order', 'duration_minutes']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'payment_status', 'enrolled_at']
    list_filter = ['payment_status']
