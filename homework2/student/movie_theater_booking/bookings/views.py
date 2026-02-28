import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from rest_framework import viewsets, status, serializers as drf_serializers
from rest_framework.response import Response
from .models import Movie, Seat, Booking, THEATER_LAYOUT
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer


# ─── DRF ViewSets ───────────────────────────────────────────────────────────────

class MovieViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on Movies."""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SeatViewSet(viewsets.ModelViewSet):
    """ViewSet for seat availability and booking."""
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for booking seats and viewing booking history."""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        seats = serializer.validated_data.get('seats', [])
        movie = serializer.validated_data['movie']
        for seat in seats:
            if Booking.objects.filter(movie=movie, seats=seat).exists():
                raise drf_serializers.ValidationError({'seats': f'Seat {seat.seat_number} is already booked for this movie.'})
        serializer.save(user=self.request.user)


# ─── Template Views ─────────────────────────────────────────────────────────────

def movie_list(request):
    """Display a list of all available movies."""
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})


@login_required
def seat_booking(request, movie_id):
    """Display available seats for a movie and handle booking."""
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'POST':
        seat_ids = request.POST.getlist('seat_ids')
        if not seat_ids:
            messages.error(request, 'Please select at least one seat.')
        else:
            already_booked = []
            seats_to_book = []
            for seat_id in seat_ids:
                seat = get_object_or_404(Seat, pk=seat_id)
                if Booking.objects.filter(movie=movie, seats=seat).exists():
                    already_booked.append(seat.seat_number)
                else:
                    seats_to_book.append(seat)
            if seats_to_book:
                booking = Booking.objects.create(movie=movie, user=request.user)
                booking.seats.set(seats_to_book)
                messages.success(request, f'Successfully booked {len(seats_to_book)} seat(s) for {movie.title}!')
                return redirect('booking_history')
            if already_booked:
                messages.error(request, f'Seat(s) {", ".join(already_booked)} already booked.')

    # Build seat data grouped by row
    seats = Seat.objects.all().order_by('row', 'number')
    booked_seat_ids = set(
        Booking.objects.filter(movie=movie).values_list('seats__id', flat=True)
    )

    seat_rows = []
    current_row = None
    current_seats = []
    for seat in seats:
        if seat.row != current_row:
            if current_row is not None:
                seat_rows.append((current_row, current_seats))
            current_row = seat.row
            current_seats = []
        current_seats.append({
            'id': seat.id,
            'seat_number': seat.seat_number,
            'number': seat.number,
            'is_booked': seat.id in booked_seat_ids,
        })
    if current_row is not None:
        seat_rows.append((current_row, current_seats))

    # JSON for JavaScript
    seat_data_json = json.dumps([
        {
            'row': row,
            'seats': seats_list,
        }
        for row, seats_list in seat_rows
    ])

    return render(request, 'bookings/seat_booking.html', {
        'movie': movie,
        'seat_rows': seat_rows,
        'seat_data_json': seat_data_json,
        'max_seats': max(THEATER_LAYOUT.values()),
    })


@login_required
def booking_history(request):
    """Display the booking history for the logged-in user."""
    bookings = Booking.objects.filter(user=request.user).select_related('movie').prefetch_related('seats')
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})


def register_view(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('movie_list')
    else:
        form = AuthenticationForm()
    return render(request, 'bookings/login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('movie_list')
