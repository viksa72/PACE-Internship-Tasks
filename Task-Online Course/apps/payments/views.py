import paypalrestsdk
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from apps.courses.models import Course, Enrollment
from .models import Payment


def get_paypal_api():
    paypalrestsdk.configure({
        'mode': settings.PAYPAL_MODE,
        'client_id': settings.PAYPAL_CLIENT_ID,
        'client_secret': settings.PAYPAL_CLIENT_SECRET,
    })
    return paypalrestsdk


@login_required
def create_payment(request, course_id):
    """Initiate a PayPal payment for course enrollment."""
    if not request.user.is_student:
        messages.error(request, 'Only students can purchase courses.')
        return redirect('courses:catalog')

    course = get_object_or_404(Course, pk=course_id, is_published=True)

    # Check if already enrolled
    if Enrollment.objects.filter(
        student=request.user, course=course, payment_status='completed'
    ).exists():
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('courses:course_detail', slug=course.slug)

    # Create or reuse pending enrollment
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course,
        defaults={'payment_status': 'pending'}
    )

    api = get_paypal_api()
    payment = api.Payment({
        'intent': 'sale',
        'payer': {'payment_method': 'paypal'},
        'redirect_urls': {
            'return_url': request.build_absolute_uri('/payments/execute/'),
            'cancel_url': request.build_absolute_uri('/payments/cancel/'),
        },
        'transactions': [{
            'item_list': {
                'items': [{
                    'name': course.title[:127],
                    'sku': str(course.pk),
                    'price': str(course.price),
                    'currency': 'USD',
                    'quantity': 1,
                }]
            },
            'amount': {'total': str(course.price), 'currency': 'USD'},
            'description': f'Enrollment in {course.title}',
        }],
    })

    if payment.create():
        # Save Payment record
        Payment.objects.update_or_create(
            enrollment=enrollment,
            defaults={
                'paypal_payment_id': payment.id,
                'amount': course.price,
                'status': 'created',
            }
        )
        # Store in session for execute step
        request.session['paypal_payment_id'] = payment.id
        request.session['paypal_enrollment_id'] = enrollment.pk

        # Redirect to PayPal approval
        for link in payment.links:
            if link.rel == 'approval_url':
                return redirect(link.href)
        messages.error(request, 'Could not find PayPal approval URL.')
    else:
        messages.error(request, f'PayPal error: {payment.error}')

    return redirect('courses:course_detail', slug=course.slug)


@login_required
def execute_payment(request):
    """Handle PayPal callback after user approves payment."""
    payment_id = request.GET.get('paymentId') or request.session.get('paypal_payment_id')
    payer_id = request.GET.get('PayerID')
    enrollment_id = request.session.get('paypal_enrollment_id')

    if not payment_id or not payer_id or not enrollment_id:
        messages.error(request, 'Payment session expired. Please try again.')
        return redirect('courses:catalog')

    enrollment = get_object_or_404(Enrollment, pk=enrollment_id, student=request.user)

    api = get_paypal_api()
    payment = api.Payment.find(payment_id)

    if payment.execute({'payer_id': payer_id}):
        # Mark enrollment as completed
        enrollment.payment_status = 'completed'
        enrollment.save()

        # Update payment record
        Payment.objects.filter(enrollment=enrollment).update(
            paypal_payer_id=payer_id,
            status='completed',
        )

        # Clean up session
        request.session.pop('paypal_payment_id', None)
        request.session.pop('paypal_enrollment_id', None)

        # Send confirmation notification
        from apps.notifications.utils import create_notification
        create_notification(
            recipient=request.user,
            title=f'Enrollment confirmed: {enrollment.course.title}',
            message=(
                f'Your payment of ${enrollment.course.price} was successful. '
                f'You are now enrolled in "{enrollment.course.title}".'
            ),
            notification_type='payment',
            link=f'/courses/{enrollment.course.slug}/',
        )

        messages.success(request, f'Payment successful! You are now enrolled in "{enrollment.course.title}".')
        return render(request, 'payments/success.html', {'enrollment': enrollment})
    else:
        enrollment.payment_status = 'failed'
        enrollment.save()
        Payment.objects.filter(enrollment=enrollment).update(status='failed')
        messages.error(request, f'Payment failed: {payment.error}')
        return render(request, 'payments/cancel.html', {'course': enrollment.course})


@login_required
def cancel_payment(request):
    """Handle PayPal cancellation."""
    enrollment_id = request.session.pop('paypal_enrollment_id', None)
    request.session.pop('paypal_payment_id', None)

    course = None
    if enrollment_id:
        enrollment = Enrollment.objects.filter(pk=enrollment_id).first()
        if enrollment:
            enrollment.payment_status = 'failed'
            enrollment.save()
            course = enrollment.course

    messages.warning(request, 'Payment was cancelled.')
    return render(request, 'payments/cancel.html', {'course': course})
