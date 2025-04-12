import uuid
from django.db import models

class Venue(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Название"
    )

    class Meta:
        verbose_name = "Площадка"
        verbose_name_plural = "Площадки"

    def __str__(self):
        return self.name

class Event(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Открыто'
        CLOSED = 'closed', 'Закрыто'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Название"
    )
    date = models.DateTimeField(  # Исправлено с data на date
        verbose_name="Дата проведения"
    )
    status = models.CharField(
        verbose_name="Статус",
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN
    )
    venue = models.ForeignKey(
        Venue,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Площадка"
    )

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ['-date']  # Сортировка по дате по умолчанию

    def __str__(self):
        return f"{self.name} ({self.date.strftime('%Y-%m-%d')})"