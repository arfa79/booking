from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Room, Hotel, Booking
from datetime import datetime, timedelta
import json

class SimpleBookingTest(TestCase):
    def setUp(self):
        # Create a hotel and a room
        self.hotel = Hotel.objects.create(name="hotel transilvania", location="Tehran")
        self.room = Room.objects.create(hotel=self.hotel, room_number="101")

        # Create a user
        self.user = User.objects.create_user(username="alireza", password="666666")

        # Set up an API client and authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Define booking data
        self.start_at = datetime.now()
        self.end_at = self.start_at + timedelta(hours=2)
        self.booking_data = {
            "room": self.room.id,
            "start_at": self.start_at.isoformat(),
            "end_at": self.end_at.isoformat(),
        }

        # URL for booking view
        self.booking_url = reverse('booking')  # Make sure 'booking' matches your URL name

    def test_successful_room_booking(self):
        """
        Test that a user can successfully book a room.
        """
        # Send POST request to book the room
        response = self.client.post(
            self.booking_url, 
            data=json.dumps(self.booking_data), 
            content_type="application/json"
        )

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.data)
        self.assertIn("booking_id", response.data)

        # Check that the booking was created in the database
        booking_exists = Booking.objects.filter(
            user=self.user,
            room=self.room,
            start_at=self.start_at,
            end_at=self.end_at
        ).exists()
        self.assertTrue(booking_exists, "The booking should exist in the database.")

        print("Room booking test passed: The room was successfully reserved.")
