from django.db import models
from django.contrib.auth.models import User


# Standard theater layout: rows A-H with varying seat counts
THEATER_LAYOUT = {
    'A': 12,
    'B': 14,
    'C': 14,
    'D': 16,
    'E': 16,
    'F': 16,
    'G': 16,
    'H': 16,
}


class Movie(models.Model):
    """Represents a movie available for booking."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.title


class Seat(models.Model):
    """Represents a seat in the theater."""
    seat_number = models.CharField(max_length=10, unique=True)
    row = models.CharField(max_length=1, default='A')
    number = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['row', 'number']

    def __str__(self):
        return f"Seat {self.seat_number}"


class Booking(models.Model):
    """Represents a booking linking a user, movie, and seat."""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'seat')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - Seat {self.seat.seat_number}"
