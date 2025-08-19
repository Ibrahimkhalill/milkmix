from django.urls import path
from . import views

urlpatterns = [
    path("revenuecat-webhook/", views.revenuecat_webhook, name="revenuecat_webhook"),
    path("me/", views.get_subscription, name="get_subscription"),
    path("all-subscriptions/", views.get_all_subscription, name="get_all_subscription"),
    path("plans/", views.get_all_plan, name="get_all_plan"),
]
