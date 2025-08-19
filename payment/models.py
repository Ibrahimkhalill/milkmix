from django.db import models
from django.conf import settings


class SubscriptionPlan(models.Model):
    DURATION_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    name = models.CharField(max_length=50, unique=True)  # e.g. Personal Plan, Consultant Plan
    revenuecat_product_id = models.CharField(max_length=200, unique=True, null=True, blank=True)  # product id from App Store / Play Store
    entitlement_id = models.CharField(max_length=200, blank=True, null=True)  # RevenueCat Entitlement ID
    duration_type = models.CharField(max_length=10, choices=DURATION_CHOICES, default='monthly')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # optional (RevenueCat sends actual)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.duration_type})"


class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    
    # RevenueCat identifiers
    app_user_id = models.CharField(max_length=255,blank=True, null=True)  # maps to your Django User.id or email
    original_app_user_id = models.CharField(max_length=255, blank=True, null=True)  # from RevenueCat
    transaction_id = models.CharField(max_length=255, blank=True, null=True)  # Apple / Google purchase id
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    auto_renew = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name if self.plan else 'Unknown'} ({self.status})"
