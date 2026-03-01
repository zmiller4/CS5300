from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date
from .models import Movie, Seat, Booking, THEATER_LAYOUT


# ─── Model Unit Tests ────────────────────────────────────────────────────────────

class MovieModelTest(TestCase):
    """Unit tests for the Movie model."""

    def setUp(self):
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='A test movie description.',
            release_date=date(2025, 1, 1),
            duration=120
        )

    def test_movie_creation(self):
        """Test that a movie is created with the correct fields."""
        self.assertEqual(self.movie.title, 'Test Movie')
        self.assertEqual(self.movie.description, 'A test movie description.')
        self.assertEqual(self.movie.release_date, date(2025, 1, 1))
        self.assertEqual(self.movie.duration, 120)

    def test_movie_str(self):
        """Test the string representation of a movie."""
        self.assertEqual(str(self.movie), 'Test Movie')


class SeatModelTest(TestCase):
    """Unit tests for the Seat model."""

    def test_seats_are_prepopulated(self):
        """Test that the standard theater seats exist from migration."""
        total_expected = sum(THEATER_LAYOUT.values())
        self.assertEqual(Seat.objects.count(), total_expected)

    def test_seat_rows_exist(self):
        """Test that all rows A-H exist."""
        for row in THEATER_LAYOUT:
            count = Seat.objects.filter(row=row).count()
            self.assertEqual(count, THEATER_LAYOUT[row])

    def test_seat_str(self):
        """Test the string representation of a seat."""
        seat = Seat.objects.get(seat_number='A1')
        self.assertEqual(str(seat), 'Seat A1')

    def test_seat_unique_number(self):
        """Test that seat numbers must be unique."""
        with self.assertRaises(Exception):
            Seat.objects.create(seat_number='A1', row='A', number=1)

    def test_seat_ordering(self):
        """Test that seats are ordered by row then number."""
        seats = list(Seat.objects.all())
        self.assertEqual(seats[0].seat_number, 'A1')
        self.assertEqual(seats[-1].seat_number, 'H16')

    def test_seat_default_is_booked(self):
        """Test that seats default to not booked."""
        seat = Seat.objects.get(seat_number='A1')
        self.assertFalse(seat.is_booked)


class BookingModelTest(TestCase):
    """Unit tests for the Booking model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Description',
            release_date=date(2025, 1, 1),
            duration=90
        )
        self.seat = Seat.objects.get(seat_number='B2')
        self.booking = Booking.objects.create(
            movie=self.movie,
            user=self.user
        )
        self.booking.seats.set([self.seat])

    def test_booking_creation(self):
        """Test that a booking is created with correct relationships."""
        self.assertEqual(self.booking.movie, self.movie)
        self.assertIn(self.seat, self.booking.seats.all())
        self.assertEqual(self.booking.user, self.user)
        self.assertIsNotNone(self.booking.booking_date)

    def test_booking_str(self):
        """Test the string representation of a booking."""
        expected = 'testuser - Test Movie - Seats B2'
        self.assertEqual(str(self.booking), expected)


# ─── API Integration Tests ──────────────────────────────────────────────────────

class MovieAPITest(APITestCase):
    """Integration tests for the Movie API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.movie = Movie.objects.create(
            title='API Movie',
            description='API test movie.',
            release_date='2025-06-15',
            duration=150
        )

    def test_list_movies(self):
        """Test listing all movies via API."""
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'API Movie')

    def test_create_movie(self):
        """Test creating a movie via API."""
        data = {
            'title': 'New Movie',
            'description': 'A brand new movie.',
            'release_date': '2025-12-25',
            'duration': 100
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)
        self.assertEqual(response.data['title'], 'New Movie')

    def test_retrieve_movie(self):
        """Test retrieving a single movie via API."""
        response = self.client.get(reverse('movie-detail', args=[self.movie.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Movie')

    def test_update_movie(self):
        """Test updating a movie via API."""
        data = {
            'title': 'Updated Movie',
            'description': 'Updated description.',
            'release_date': '2025-06-15',
            'duration': 160
        }
        response = self.client.put(reverse('movie-detail', args=[self.movie.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, 'Updated Movie')

    def test_delete_movie(self):
        """Test deleting a movie via API."""
        response = self.client.delete(reverse('movie-detail', args=[self.movie.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)

    def test_create_movie_missing_fields(self):
        """Test creating a movie with missing required fields returns 400."""
        data = {'title': 'Incomplete Movie'}
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SeatAPITest(APITestCase):
    """Integration tests for the Seat API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_list_seats(self):
        """Test listing all seats via API."""
        response = self.client.get(reverse('seat-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        total_expected = sum(THEATER_LAYOUT.values())
        self.assertEqual(len(response.data), total_expected)

    def test_retrieve_seat(self):
        """Test retrieving a single seat via API."""
        seat = Seat.objects.get(seat_number='C3')
        response = self.client.get(reverse('seat-detail', args=[seat.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['seat_number'], 'C3')

    def test_seat_has_row_and_number(self):
        """Test that seats have row and number fields."""
        seat = Seat.objects.get(seat_number='D5')
        response = self.client.get(reverse('seat-detail', args=[seat.id]))
        self.assertEqual(response.data['row'], 'D')
        self.assertEqual(response.data['number'], 5)


class BookingAPITest(APITestCase):
    """Integration tests for the Booking API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='bookuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.movie = Movie.objects.create(
            title='Booking Movie',
            description='A movie for booking tests.',
            release_date='2025-03-01',
            duration=110
        )
        self.seat = Seat.objects.get(seat_number='E5')

    def test_create_booking(self):
        """Test creating a booking via API."""
        data = {'movie': self.movie.id, 'seats': [self.seat.id]}
        response = self.client.post(reverse('booking-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_create_booking_already_booked_seat(self):
        """Test booking an already booked seat returns error."""
        booking = Booking.objects.create(movie=self.movie, user=self.user)
        booking.seats.set([self.seat])
        data = {'movie': self.movie.id, 'seats': [self.seat.id]}
        response = self.client.post(reverse('booking-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_bookings(self):
        """Test listing bookings via API."""
        booking = Booking.objects.create(movie=self.movie, user=self.user)
        booking.seats.set([self.seat])
        response = self.client.get(reverse('booking-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_booking(self):
        """Test retrieving a single booking via API."""
        booking = Booking.objects.create(movie=self.movie, user=self.user)
        booking.seats.set([self.seat])
        response = self.client.get(reverse('booking-detail', args=[booking.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['movie'], self.movie.id)

    def test_booking_sets_user_automatically(self):
        """Test that the booking user is set to the authenticated user."""
        data = {'movie': self.movie.id, 'seats': [self.seat.id]}
        response = self.client.post(reverse('booking-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.first()
        self.assertEqual(booking.user, self.user)


# ─── Template View Tests ────────────────────────────────────────────────────────

class MovieListViewTest(TestCase):
    """Tests for the movie list template view."""

    def setUp(self):
        self.client = Client()
        self.movie = Movie.objects.create(
            title='View Movie',
            description='A movie for view tests.',
            release_date=date(2025, 5, 1),
            duration=95
        )

    def test_movie_list_page_loads(self):
        """Test that the movie list page loads successfully."""
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/movie_list.html')

    def test_movie_list_contains_movie(self):
        """Test that the movie list page displays movies."""
        response = self.client.get(reverse('movie_list'))
        self.assertContains(response, 'View Movie')

    def test_movie_list_empty(self):
        """Test the movie list page when no movies exist."""
        Movie.objects.all().delete()
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No movies available')


class SeatBookingViewTest(TestCase):
    """Tests for the seat booking template view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewuser', password='testpass123')
        self.client.login(username='viewuser', password='testpass123')
        self.movie = Movie.objects.create(
            title='Booking View Movie',
            description='Description',
            release_date=date(2025, 4, 15),
            duration=100
        )
        self.seat = Seat.objects.get(seat_number='F6')

    def test_seat_booking_page_loads(self):
        """Test that the seat booking page loads for authenticated users."""
        response = self.client.get(reverse('book_seat', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/seat_booking.html')

    def test_seat_booking_requires_login(self):
        """Test that the seat booking page requires authentication."""
        self.client.logout()
        response = self.client.get(reverse('book_seat', args=[self.movie.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_seat_booking_post(self):
        """Test booking a seat through the form."""
        response = self.client.post(
            reverse('book_seat', args=[self.movie.id]),
            {'seat_ids': [self.seat.id]}
        )
        self.assertEqual(response.status_code, 302)  # Redirect to history
        self.assertEqual(Booking.objects.count(), 1)

    def test_seat_booking_multiple_seats(self):
        """Test booking multiple seats at once creates a single booking."""
        seat2 = Seat.objects.get(seat_number='F7')
        response = self.client.post(
            reverse('book_seat', args=[self.movie.id]),
            {'seat_ids': [self.seat.id, seat2.id]}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.seats.count(), 2)

    def test_seat_booking_already_booked(self):
        """Test booking an already booked seat shows error."""
        booking = Booking.objects.create(movie=self.movie, user=self.user)
        booking.seats.set([self.seat])
        response = self.client.post(
            reverse('book_seat', args=[self.movie.id]),
            {'seat_ids': [self.seat.id]}
        )
        self.assertEqual(response.status_code, 200)  # Stays on page
        self.assertEqual(Booking.objects.count(), 1)  # No new booking

    def test_seat_booking_invalid_movie(self):
        """Test booking with non-existent movie returns 404."""
        response = self.client.get(reverse('book_seat', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_seat_marked_as_booked_after_booking(self):
        """Test that seat is_booked field is set to True after booking."""
        self.client.post(
            reverse('book_seat', args=[self.movie.id]),
            {'seat_ids': [self.seat.id]}
        )
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)


class BookingHistoryViewTest(TestCase):
    """Tests for the booking history template view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='historyuser', password='testpass123')
        self.client.login(username='historyuser', password='testpass123')
        self.movie = Movie.objects.create(
            title='History Movie',
            description='Description',
            release_date=date(2025, 7, 1),
            duration=85
        )
        self.seat = Seat.objects.get(seat_number='G7')

    def test_booking_history_page_loads(self):
        """Test that the booking history page loads for authenticated users."""
        response = self.client.get(reverse('booking_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_history.html')

    def test_booking_history_requires_login(self):
        """Test that the booking history page requires authentication."""
        self.client.logout()
        response = self.client.get(reverse('booking_history'))
        self.assertEqual(response.status_code, 302)

    def test_booking_history_shows_user_bookings(self):
        """Test that only the logged-in user's bookings are shown."""
        booking = Booking.objects.create(movie=self.movie, user=self.user)
        booking.seats.set([self.seat])
        response = self.client.get(reverse('booking_history'))
        self.assertContains(response, 'History Movie')

    def test_booking_history_empty(self):
        """Test the booking history page when user has no bookings."""
        response = self.client.get(reverse('booking_history'))
        self.assertContains(response, 'You have no bookings yet')

    def test_booking_history_excludes_other_users(self):
        """Test that other users' bookings are not shown."""
        other_user = User.objects.create_user(username='other', password='testpass123')
        booking = Booking.objects.create(movie=self.movie, user=other_user)
        booking.seats.set([self.seat])
        response = self.client.get(reverse('booking_history'))
        self.assertNotContains(response, 'History Movie')


# ─── Authentication Tests ───────────────────────────────────────────────────────

class AuthenticationTest(TestCase):
    """Tests for registration, login, and logout."""

    def setUp(self):
        self.client = Client()

    def test_register_page_loads(self):
        """Test that the registration page loads."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/register.html')

    def test_register_user(self):
        """Test user registration via form."""
        data = {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_password_mismatch(self):
        """Test registration with mismatched passwords."""
        data = {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass456!',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)  # Stays on page
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_login_page_loads(self):
        """Test that the login page loads."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/login.html')

    def test_login_user(self):
        """Test user login via form."""
        User.objects.create_user(username='loginuser', password='testpass123')
        data = {'username': 'loginuser', 'password': 'testpass123'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # Redirect on success

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {'username': 'nobody', 'password': 'wrongpass'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)  # Stays on page

    def test_logout(self):
        """Test user logout."""
        User.objects.create_user(username='logoutuser', password='testpass123')
        self.client.login(username='logoutuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect on logout
