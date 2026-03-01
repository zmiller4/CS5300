from django.contrib import admin
from .models import Movie, Seat, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'duration')
    search_fields = ('title',)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'row', 'number', 'is_booked')
    list_filter = ('row', 'is_booked')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'get_seats', 'user', 'booking_date')
    list_filter = ('movie', 'booking_date')

    def get_seats(self, obj):
        return ', '.join(s.seat_number for s in obj.seats.all())
    get_seats.short_description = 'Seats'
