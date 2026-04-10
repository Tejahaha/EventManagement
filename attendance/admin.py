from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['registration', 'attendance_status', 'marked_at']
    list_filter = ['attendance_status']
