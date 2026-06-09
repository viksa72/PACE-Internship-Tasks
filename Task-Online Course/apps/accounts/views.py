import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import CustomUser, OTPToken, TeacherProfile, StudentProfile
from .forms import (
    StudentSignupForm, TeacherSignupForm, LoginForm,
    OTPVerifyForm, TeacherProfileForm, StudentProfileForm
)


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def send_otp_email(user, otp_token):
    subject = 'LearnHub — Your One-Time Password'
    message = f"""
Hello {user.first_name or user.username},

Your LearnHub login OTP is:

    {otp_token}

This code expires in 10 minutes. Do not share it with anyone.

— The LearnHub Team
"""
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)


def student_signup(request):
    if request.user.is_authenticated:
        return redirect('courses:catalog')
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created! Please log in.')
            return redirect('accounts:login')
    else:
        form = StudentSignupForm()
    return render(request, 'accounts/student_signup.html', {'form': form})


def teacher_signup(request):
    if request.user.is_authenticated:
        return redirect('courses:catalog')
    if request.method == 'POST':
        form = TeacherSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Update teacher profile with extra fields
            if hasattr(user, 'teacher_profile'):
                user.teacher_profile.bio = form.cleaned_data.get('bio', '')
                user.teacher_profile.expertise = form.cleaned_data.get('expertise', '')
                user.teacher_profile.save()
            messages.success(request, 'Teacher account created! Please log in.')
            return redirect('accounts:login')
    else:
        form = TeacherSignupForm()
    return render(request, 'accounts/teacher_signup.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('courses:catalog')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                # Invalidate old OTPs
                OTPToken.objects.filter(user=user, is_used=False).update(is_used=True)
                # Generate + send new OTP
                otp_code = generate_otp()
                OTPToken.objects.create(user=user, token=otp_code)
                try:
                    send_otp_email(user, otp_code)
                    messages.info(request, f'OTP sent to {user.email}. Check your inbox.')
                except Exception:
                    messages.warning(request, f'Email sending failed. Your OTP is: {otp_code}')
                # Store user id in session for OTP step
                request.session['pre_otp_user_id'] = user.pk
                return redirect('accounts:otp_verify')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def otp_verify(request):
    user_id = request.session.get('pre_otp_user_id')
    if not user_id:
        return redirect('accounts:login')

    user = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            token = OTPToken.objects.filter(
                user=user, token=entered_otp, is_used=False
            ).order_by('-created_at').first()

            if token and token.is_valid():
                token.is_used = True
                token.save()
                login(request, user, backend='apps.accounts.backends.EmailBackend')
                del request.session['pre_otp_user_id']
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                if user.is_teacher:
                    return redirect('courses:teacher_dashboard')
                return redirect('courses:catalog')
            else:
                messages.error(request, 'Invalid or expired OTP. Please try again.')
    else:
        form = OTPVerifyForm()

    return render(request, 'accounts/otp_verify.html', {'form': form, 'email': user.email})


def resend_otp(request):
    user_id = request.session.get('pre_otp_user_id')
    if not user_id:
        return redirect('accounts:login')
    user = get_object_or_404(CustomUser, pk=user_id)
    OTPToken.objects.filter(user=user, is_used=False).update(is_used=True)
    otp_code = generate_otp()
    OTPToken.objects.create(user=user, token=otp_code)
    try:
        send_otp_email(user, otp_code)
        messages.info(request, 'A new OTP has been sent to your email.')
    except Exception:
        messages.warning(request, f'Email sending failed. Your OTP is: {otp_code}')
    return redirect('accounts:otp_verify')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def profile(request):
    user = request.user
    if user.is_teacher:
        profile_obj, _ = TeacherProfile.objects.get_or_create(user=user)
        if request.method == 'POST':
            form = TeacherProfileForm(request.POST, request.FILES, instance=profile_obj)
            if form.is_valid():
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('accounts:profile')
        else:
            form = TeacherProfileForm(
                instance=profile_obj,
                initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}
            )
        return render(request, 'accounts/teacher_profile.html', {'form': form, 'profile': profile_obj})
    else:
        profile_obj, _ = StudentProfile.objects.get_or_create(user=user)
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, request.FILES, instance=profile_obj)
            if form.is_valid():
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('accounts:profile')
        else:
            form = StudentProfileForm(
                instance=profile_obj,
                initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}
            )
        return render(request, 'accounts/student_profile.html', {'form': form, 'profile': profile_obj})
