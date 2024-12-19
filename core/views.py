import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer
from django.core.exceptions import ValidationError
from .responses import bad_request_response, internal_server_error_response, success_response

logger = logging.getLogger(__name__)

class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Log the request for debugging purposes
        logger.info(f"User {request.user.username} is attempting to create a booking.")

        serializer = BookingSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            try:
                booking = Booking.create_booking(
                    user=request.user,
                    room=serializer.validated_data['room'],
                    start_at=serializer.validated_data['start_at'],
                    end_at=serializer.validated_data['end_at']
                )
                return success_response({"message": "Booking successful!", "booking_id": booking.id})
            except ValidationError as e:
                logger.warning(f"Validation error: {str(e)}")
                return bad_request_response(str(e))  # Returns 400 error
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return internal_server_error_response("An unexpected error occurred.")  # Returns 500 error
        
        logger.warning(f"Invalid serializer data: {serializer.errors}")
        return bad_request_response(serializer.errors)  # Returns 400 error for invalid serializer
