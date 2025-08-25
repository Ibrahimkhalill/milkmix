from django.urls import path
from . import views

urlpatterns = [
    path('milk-history/create/', views.create_milk_history, name='create_milk_history'),
    path('milk-history/', views.list_milk_history, name='list_milk_history'),
    path('milk-history/<int:pk>/', views.milk_history_detail, name='milk_history_detail'),
    path('milk-history/user/<int:user_id>/', views.list_milk_history_by_user, name='list_milk_history_by_user'),
    path('milk-history/user/delete/', views.delete_all_history, name='delete_all_history'),
]