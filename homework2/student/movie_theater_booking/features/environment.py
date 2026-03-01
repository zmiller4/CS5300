"""Behave-Django environment configuration."""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_theater_booking.settings')

import django
django.setup()

from django.test import Client
from bookings.models import Seat, THEATER_LAYOUT


def before_scenario(context, scenario):
    """Set up a fresh Django test client and ensure seats exist for each scenario."""
    context.client = Client()
    # Repopulate theater seats (behave-django flushes DB between scenarios)
    if Seat.objects.count() == 0:
        for row_letter, seat_count in THEATER_LAYOUT.items():
            for num in range(1, seat_count + 1):
                Seat.objects.create(
                    seat_number=f"{row_letter}{num}",
                    row=row_letter,
                    number=num,
                )
