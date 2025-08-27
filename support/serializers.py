# support/serializers.py
from rest_framework import serializers
from .models import SupportRequest
from notifications.models import Notification
class SupportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = ['id', 'email', 'problem', 'description', 'created_at']
        
        
        read_only_fields = ['id', 'created_at']
        
        