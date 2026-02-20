from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from rest_framework import viewsets, status, serializers as drf_serializers
from rest_framework.response import Response
from .models import Movie, Seat, Booking
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
        seat = serializer.validated_data['seat']
        if seat.is_booked:
            raise drf_serializers.ValidationError({'seat': 'This seat is already booked.'})
        seat.is_booked = True
        seat.save()
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
    seats = Seat.objects.all()

    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        seat = get_object_or_404(Seat, pk=seat_id)

        if seat.is_booked:
            messages.error(request, 'This seat is already booked.')
        else:
            Booking.objects.create(movie=movie, seat=seat, user=request.user)
            seat.is_booked = True
            seat.save()
            messages.success(request, f'Successfully booked Seat {seat.seat_number} for {movie.title}!')
            return redirect('booking_history')

    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})


@login_required
def booking_history(request):
    """Display the booking history for the logged-in user."""
    bookings = Booking.objects.filter(user=request.user).select_related('movie', 'seat')
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
