from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['room', 'start_at', 'end_at']

    def validate(self, attrs):
        # This validation can be kept if you want to check for overlaps before creating/updating
        room = attrs.get('room')
        start_at = attrs.get('start_at')
        end_at = attrs.get('end_at')

        # Check for overlapping bookings
        if Booking.objects.filter(
            room=room,
            start_at__lt=end_at,
            end_at__gt=start_at
        ).exists():
            raise serializers.ValidationError("Room is already booked for the given dates.")

        return attrs
