from django.contrib import admin
from .models import Subscription, SubscriptionPlan

# Inline admin for Description (to be displayed directly in SubscriptionPlan admin)


# SubscriptionPlan Admin
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('revenuecat_product_id', 'name', 'amount', 'duration_type', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('duration_type',)
   

# Subscription Admin
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'start_date', 'end_date', 'is_active')
    search_fields = ('user__email', 'plan__name')  # Searching by user email and plan name
    list_filter = ('status',)
    readonly_fields = ('start_date', 'end_date')

    def is_active(self, obj):
        return obj.status == 'active'
    is_active.boolean = True  # Displays as a green checkmark

# Description Admin


# Registering the models with the custom admin views
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)

