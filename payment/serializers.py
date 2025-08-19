from rest_framework import serializers
from .models import SubscriptionPlan, Subscription
from authentications.serializers import CustomUserSerializer


class SubscriptionPlanSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = SubscriptionPlan
        fields = [
            'id',
            'name',
            'amount',
            'duration_type',
            'revenuecat_product_id',
            'entitlement_id',
            'created_at',
            'updated_at',
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    plan = SubscriptionPlanSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id',
            'user',
            'plan',
            'app_user_id',
            'original_app_user_id',
            'transaction_id',
            'status',
            'start_date',
            'end_date',
            'auto_renew',
            'created_at',
            'updated_at',
        ]
