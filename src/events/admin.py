from django.contrib import admin
from .models import Venue, Event


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'status', 'venue')
    list_filter = ('status', 'venue')
    search_fields = ('name',)
    date_hierarchy = 'date'