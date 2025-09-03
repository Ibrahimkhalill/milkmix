from django.shortcuts import render

# Create your views here.
# support/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import SupportRequestSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from notifications.models import Notification
from .models import SupportRequest


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_support_request(request):
    serializer = SupportRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        Notification.objects.create(
            user=request.user if request.user.is_authenticated else None,
            title="Help Desk Request",
            message=f"New support request submitted by {serializer.validated_data.get('email')}",
            notification_type="user_management"
        )
        return Response({"message": "Support request submitted successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def submit_support_list(request):
    support = SupportRequest.objects.all().order_by('-created_at')
    serializer = SupportRequestSerializer(support, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
