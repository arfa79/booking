from django.db import models
from django.conf import settings

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, )  

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
