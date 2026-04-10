import uuid
from django.db import models
from registrations.models import Registration

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=50, unique=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = 'TXN-' + str(uuid.uuid4()).upper()[:10]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_id} - {self.payment_status}"
