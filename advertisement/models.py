import random
import string
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Advertisement(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)  # Added title field
    external_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='advertisements/', blank=True, null=True)
    target_user = models.CharField(max_length=500, blank=True,null=True)
    status = models.CharField(max_length=300, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    

    def __str__(self):
        return self.title
