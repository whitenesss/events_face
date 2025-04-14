from django.contrib import admin
from .models import SyncResult


@admin.register(SyncResult)
class SyncResultAdmin(admin.ModelAdmin):
    list_display = (
        'started_at',
        'finished_at',
        'date_filter',
        'sync_all',
        'new_events_count',
        'updated_events_count',
        'is_success'
    )
    list_filter = ('is_success', 'sync_all')
    search_fields = ('error_message',)
    readonly_fields = (
        'started_at',
        'finished_at',
        'date_filter',
        'sync_all',
        'new_events_count',
        'updated_events_count',
        'is_success',
        'error_message'
    )