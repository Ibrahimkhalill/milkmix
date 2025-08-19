from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_notifications(request):
    """
    Retrieve all notifications for the authenticated user, ordered by created_at descending.
    """
    notifications = Notification.objects.all().order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response( serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def mark_notification_as_read(request, notification_id):
    """
    Mark a specific notification as read.
    """
   
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read."}, status=200)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found."}, status=404)
