from django.contrib import admin

# Register your models here.
from .models import SupportRequest


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'problem', 'created_at')
    search_fields = ('email', 'problem')
    list_filter = ('created_at',)
    ordering = ('-created_at',)