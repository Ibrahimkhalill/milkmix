from django.contrib import admin

# Register your models here.
from .models import MilkHistory

@admin.register(MilkHistory)
class MilkHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'farm', 'created_at', 'total_volume')
    search_fields = ('user__email', 'farm__email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)