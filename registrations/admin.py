from django.contrib import admin
from .models import Registration

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['registration_id', 'user', 'event', 'registered_at', 'status']
    list_filter = ['status']
    search_fields = ['registration_id', 'user__username']
