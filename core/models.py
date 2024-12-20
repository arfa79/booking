from django.db import models, transaction, DatabaseError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.db.models import Q


class Hotel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Hotel Name"))
    location = models.CharField(max_length=200, verbose_name=_("Hotel Location"))

    def __str__(self):
        return self.name

    def clean(self):
        """
        Add custom validation for Hotel model.
        """
        if len(self.name) < 3:
            raise ValidationError(_("Hotel name must be at least 3 characters long."))


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    room_number = models.CharField(max_length=10, verbose_name=_("Room Number"))

    def __str__(self):
        return f"Room {self.room_number} - {self.hotel.name}"

    def clean(self):
        """
        Add custom validation for Room model.
        """
        if not self.room_number.isdigit():
            raise ValidationError(_("Room number must be numeric."))


class Booking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("User"))
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("Room"))
    start_at = models.DateTimeField(verbose_name=_("Start Date"))
    end_at = models.DateTimeField(verbose_name=_("End Date"))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["room", "start_at", "end_at"],
                name="unique_booking_per_room"
            )
        ]
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")

    def __str__(self):
        return f"Booking by {self.user.username} for {self.room} from {self.start_at} to {self.end_at}"

    def clean(self):
        """
        Custom validation for the Booking model.
        Ensures start date is before end date and start date is not in the past.
        """
        if self.start_at >= self.end_at:
            raise ValidationError(_("Start date must be before the end date."))

        if self.start_at < now():
            raise ValidationError(_("Start date cannot be in the past."))

    def save(self, *args, **kwargs):
        """
        Override save method to include validation.
        """
        self.clean()
        super().save(*args, **kwargs)

    @classmethod
    def create_booking(cls, user, room, start_at, end_at):
        """
        booking with validation for overlapping bookings and date constraints,
        using SELECT ... FOR UPDATE to prevent race conditions.
        """
        # Validate dates
        if start_at >= end_at:
            raise ValidationError(_("Start date must be before the end date."))

        if start_at < now():
            raise ValidationError(_("Start date cannot be in the past."))

        # Start atomic transaction
        with transaction.atomic():
            # Lock the room's existing bookings using SELECT ... FOR UPDATE
            overlapping_bookings = cls.objects.filter(
                room=room,
                start_at__lt=end_at,
                end_at__gt=start_at
            ).select_for_update()

            if overlapping_bookings.exists():
                raise ValidationError(_("Room is already booked for the given dates."))

            # Create the booking after validations and locks
            return cls.objects.create(user=user, room=room, start_at=start_at, end_at=end_at)

    def update_booking(self, start_at, end_at):
        """
        Update an existing booking with validation for overlapping bookings and date constraints,
        using SELECT ... FOR UPDATE to prevent race conditions.
        """
        # Validate dates
        if start_at >= end_at:
            raise ValidationError(_("Start date must be before the end date."))

        if start_at < now():
            raise ValidationError(_("Start date cannot be in the past."))

        with transaction.atomic():
            # Lock overlapping bookings for the same room (excluding the current booking)
            overlapping_bookings = Booking.objects.filter(
                room=self.room,
                start_at__lt=end_at,
                end_at__gt=start_at
            ).exclude(id=self.id).select_for_update()

            if overlapping_bookings.exists():
                raise ValidationError(_("Room is already booked for the given dates."))

            # Update the booking
            self.start_at = start_at
            self.end_at = end_at
            self.save()

    @staticmethod
    def is_room_available(room, start_at, end_at):
        """
        Check if a room is available for a given date range.
        """
        return not Booking.objects.filter(
            room=room,
            start_at__lt=end_at,
            end_at__gt=start_at
        ).exists()

    @staticmethod
    def sample_utility_check(name: str) -> bool:
        """
        A sample utility function to check something based on a name.
        """
        # Example logic: Check if a room with this name exists
        return Room.objects.filter(room_number=name).exists()

    @staticmethod
    def debug_overlap_check(room, start_at, end_at):
        """
        Debugging utility to check for overlapping bookings.
        """
        overlaps = Booking.objects.filter(
            room=room,
            start_at__lt=end_at,
            end_at__gt=start_at
        )
        print("Overlapping bookings:", overlaps)
        return overlaps.exists()
