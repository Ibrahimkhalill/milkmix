from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Subscription, SubscriptionPlan
from authentications.models import CustomUser
from .serializers import SubscriptionSerializer, SubscriptionPlanSerializer
import pytz
from notifications.models import Notification

@api_view(["POST"])
@permission_classes([AllowAny])  # RevenueCat webhook public
def revenuecat_webhook(request):
    """
    RevenueCat Webhook Handler
    """
    data = request.data.get("event", {})

    if not data:
        return Response({"error": "Invalid payload"}, status=400)

    event_type = data.get("type")
    app_user_id = data.get("app_user_id")
    product_id = data.get("product_id")

    if not app_user_id:
        return Response({"error": "Missing app_user_id"}, status=400)

    try:
        user = get_object_or_404(CustomUser, id=app_user_id)
    except Exception:
        return Response({"error": f"User with id {app_user_id} not found"}, status=404)

    # Time conversion
    purchased_at = data.get("purchased_at_ms")
    expiration_at = data.get("expiration_at_ms")

    purchased_at = datetime.fromtimestamp(purchased_at / 1000, tz=pytz.UTC) if purchased_at else None
    expiration_at = datetime.fromtimestamp(expiration_at / 1000, tz=pytz.UTC) if expiration_at else None

    # Find plan
    plan = None
    if product_id:
        try:
            plan = SubscriptionPlan.objects.get(revenuecat_product_id=product_id)
        except SubscriptionPlan.DoesNotExist:
            pass

    # Create or update subscription
    subscription, created = Subscription.objects.get_or_create(
        user=user,
        defaults={
            "app_user_id": app_user_id,
            "plan": plan,
            "start_date": purchased_at,
            "end_date": expiration_at,
            "status": "active" if event_type in ["INITIAL_PURCHASE", "RENEWAL"] else "expired",
            "auto_renew": event_type in ["INITIAL_PURCHASE", "RENEWAL"]
        }
    )

    if not created:
        subscription.plan = plan
        subscription.app_user_id = app_user_id
        subscription.start_date = purchased_at
        subscription.end_date = expiration_at
        subscription.status = "active" if event_type in ["INITIAL_PURCHASE", "RENEWAL"] else "expired"
        subscription.auto_renew = event_type in ["INITIAL_PURCHASE", "RENEWAL"]
        subscription.save()
    
    action = "created" if created else "updated"    
    Notification.objects.create(
        user=user,
        title="Subscription " + action.capitalize(),
        message=f"Your subscription for plan '{plan.name if plan else 'Unknown'}' has been {action}.",
        notification_type="financial"
    )

    return Response({"message": f"Subscription updated for {user.email} via {event_type}"}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subscription(request):
    """
    Retrieve subscription(s) for authenticated user.
    """
    user = request.user
    subscriptions = Subscription.objects.filter(user=user)
    if not subscriptions.exists():
        return Response({"message": "No subscription found for this user."}, status=404)

    serializer = SubscriptionSerializer(subscriptions, many=True)
    return Response({"subscriptions": serializer.data}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_subscription(request):
    """
    Retrieve all subscriptions (admin or staff use).
    """
    subscriptions = Subscription.objects.select_related('user', 'plan').all()
    serializer = SubscriptionSerializer(subscriptions, many=True)
    return Response( serializer.data, status=200)


@api_view(['GET'])
def get_all_plan(request):
    """
    Retrieve all subscription plans.
    """
    plans = SubscriptionPlan.objects.all()
    serializer = SubscriptionPlanSerializer(plans, many=True)
    return Response({"plans": serializer.data}, status=200)
