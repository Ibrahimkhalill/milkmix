from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

from authentications.serializers import CustomUserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer ()
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at']
    
    
  
        