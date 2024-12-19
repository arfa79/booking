import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Booking
from .serializers import BookingSerializer
from django.core.exceptions import ValidationError

# Configure the logger
logger = logging.getLogger(__name__)

class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                booking = Booking.create_booking(
                    user=request.user,
                    room=serializer.validated_data['room'],
                    start_at=serializer.validated_data['start_at'],
                    end_at=serializer.validated_data['end_at']
                )
                logger.info(f"Booking created successfully: {booking.id} by user: {request.user.username}")
                return Response(
                    {"message": "Booking successful!", "booking_id": booking.id},
                    status=status.HTTP_201_CREATED
                )
            except ValidationError as e:
                logger.warning(f"Validation error while creating booking: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)