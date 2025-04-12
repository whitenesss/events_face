from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer
from .filters import EventFilter
from .pagination import EventCursorPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.select_related('venue')
    serializer_class = EventSerializer
    filterset_class = EventFilter
    pagination_class = EventCursorPagination

    @method_decorator(cache_page(60*5))  # Кешируем на 5 минут
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)