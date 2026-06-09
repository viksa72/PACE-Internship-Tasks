from django import forms
from .models import Course, Topic, Lesson, Category


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'category', 'short_description', 'description',
                  'price', 'thumbnail', 'level', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'id': 'course-description'}),
            'short_description': forms.Textarea(attrs={'rows': 2}),
            'price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = '-- Select Category --'


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'order']
        widgets = {'order': forms.NumberInput(attrs={'min': '0'})}


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url', 'order', 'duration_minutes']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'id': 'lesson-content'}),
            'order': forms.NumberInput(attrs={'min': '0'}),
            'duration_minutes': forms.NumberInput(attrs={'min': '0'}),
            'video_url': forms.URLInput(attrs={'placeholder': 'https://www.youtube.com/embed/...'}),
        }
