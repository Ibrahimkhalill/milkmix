
from django.db import models

class SupportRequest(models.Model):
    email = models.EmailField(blank=True, null=True)
    problem = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.problem}"
