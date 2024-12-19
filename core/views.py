from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework import status
from .models import Room, Booking
from .serializers import BookingSerializer

class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.validated_data['room']
            start_at = serializer.validated_data['start_at']
            end_at = serializer.validated_data['end_at']

            # Check for overlapping bookings
            with transaction.atomic():
                if Booking.objects.filter(
                    room=room,
                    start_at__lt=end_at,
                    end_at__gt=start_at
                ).exists():
                    return Response(
                        {"error": "Room is already booked for the given dates."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # Create booking
                booking = Booking.objects.create(
                    user=request.user,
                    room=room,
                    start_at=start_at,
                    end_at=end_at
                )
                return Response(
                    {"message": "Booking successful!", "booking_id": booking.id},
                    status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)