from rest_framework import serializers
from .models import Venue, Event



class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ('id', 'name')


class EventSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'status', 'venue')
