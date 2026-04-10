from django.db import models
from django.conf import settings
from lockers.models import Locker
import logging

logger = logging.getLogger(__name__)


class Reservation(models.Model):
    """Reservation model for tracking locker bookings"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    locker = models.ForeignKey(
        Locker,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    reserved_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservation #{self.id} - {self.user.username} - Locker {self.locker.locker_number} ({self.status})"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['locker', 'status']),
        ]

    def save(self, *args, **kwargs):
        logger.info(f"Saving reservation: {self.id}, User: {self.user.username}, Status: {self.status}")
        super().save(*args, **kwargs)
