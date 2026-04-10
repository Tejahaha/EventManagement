import uuid
from django.db import models
from accounts.models import CustomUser
from events.models import Event

class Registration(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registration_id = models.CharField(max_length=20, unique=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.registration_id:
            self.registration_id = 'REG-' + str(uuid.uuid4()).upper()[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.registration_id} - {self.user.username} @ {self.event.title}"

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-registered_at']
