from django.db import models
from django.utils import timezone
from uuid import uuid4


class SyncResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    date_filter = models.DateField(null=True, blank=True)
    sync_all = models.BooleanField(default=False)
    new_events_count = models.PositiveIntegerField(default=0)
    updated_events_count = models.PositiveIntegerField(default=0)
    is_success = models.BooleanField(default=False)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Результат синхронизации'
        verbose_name_plural = 'Результаты синхронизации'

    def __str__(self):
        return f"Синхронизация от {self.started_at.strftime('%Y-%m-%d %H:%M')}"