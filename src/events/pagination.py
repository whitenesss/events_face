from rest_framework.pagination import CursorPagination
from rest_framework.response import Response

class EventCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-date'
    cursor_query_param = 'cursor'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'events': data
        })