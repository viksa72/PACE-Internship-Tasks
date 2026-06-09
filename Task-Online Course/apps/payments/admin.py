from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'paypal_payment_id', 'amount', 'status', 'created_at']
    list_filter = ['status', 'currency']
    search_fields = ['paypal_payment_id', 'enrollment__student__username']
