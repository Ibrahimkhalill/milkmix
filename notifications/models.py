from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    """
    Notification model to send messages or alerts to users.
    """

    NOTIFICATION_TYPE_CHOICES = [
        ('user_management', 'User Management'),
        ('financial', 'Financial'),
        ('system', 'System'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications' , blank=True, null=True)  # Added user field
    title = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.title or self.message[:20]} ({'Read' if self.is_read else 'Unread'})"
