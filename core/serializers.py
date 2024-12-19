from rest_framework import serializers
from .models import Booking, Hotel

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['room', 'start_at', 'end_at']