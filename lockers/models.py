from django.db import models
import logging

logger = logging.getLogger(__name__)


class Locker(models.Model):
    """Locker model for managing storage lockers"""
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
        ('deactivated', 'Deactivated'),
    )
    
    locker_number = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    size = models.CharField(max_length=20, default='medium', help_text="Small, Medium, Large")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Locker {self.locker_number} - {self.location} ({self.status})"

    class Meta:
        ordering = ['locker_number']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['locker_number']),
        ]

    def save(self, *args, **kwargs):
        logger.info(f"Saving locker: {self.locker_number}, Status: {self.status}")
        super().save(*args, **kwargs)
