# support/urls.py
from django.urls import path
from .views import submit_support_request , submit_support_list

urlpatterns = [
    path('submit/', submit_support_request, name='submit-support'),
    path('list/', submit_support_list, name='support-list'),
    
]
