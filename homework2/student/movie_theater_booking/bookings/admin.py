from django.contrib import admin
from .models import Movie, Seat, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'duration')
    search_fields = ('title',)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'row', 'number')
    list_filter = ('row',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'seat', 'user', 'booking_date')
    list_filter = ('movie', 'booking_date')
