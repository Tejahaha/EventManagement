from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'registration', 'amount', 'payment_status', 'payment_date']
    list_filter = ['payment_status']
