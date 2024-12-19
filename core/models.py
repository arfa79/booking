from django.db import models, transaction
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class Hotel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Hotel Name"))
    location = models.CharField(max_length=200, verbose_name=_("Hotel Location"))  

    def __str__(self): 
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    room_number = models.CharField(max_length=10)

    def __str__(self): 
        return f"Room {self.room_number} - {self.hotel.name}"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["room", "start_at", "end_at"],
                name="unique_booking_per_room"
            )
        ]

    def __str__(self): 
        return f"Booking by {self.user.username} for {self.room} from {self.start_at} to {self.end_at}"

    @classmethod
    def create_booking(cls, user, room, start_at, end_at):
        # Check for overlapping bookings
        if cls.objects.filter(
            room=room,
            start_at__lt=end_at,
            end_at__gt=start_at
        ).exists():
            raise ValidationError("Room is already booked for the given dates.")

        # Use atomic transaction to ensure the booking creation is safe
        with transaction.atomic():
            return cls.objects.create(user=user, room=room, start_at=start_at, end_at=end_at)

    def update_booking(self, start_at, end_at):
        # Check for overlapping bookings
        if Booking.objects.filter(
            room=self.room,
            start_at__lt=end_at,
            end_at__gt=start_at
        ).exclude(id=self.id).exists():
            raise ValidationError("Room is already booked for the given dates.")

        # Update the booking details
        with transaction.atomic():
            self.start_at = start_at
            self.end_at = end_at
            self.save()
