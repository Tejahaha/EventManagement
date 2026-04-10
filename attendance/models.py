from django.db import models
from registrations.models import Registration

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name='attendance')
    attendance_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='absent')
    marked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.registration.user.username} - {self.attendance_status}"
