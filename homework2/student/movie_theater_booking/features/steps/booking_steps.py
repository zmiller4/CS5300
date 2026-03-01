from behave import given, when, then
from django.urls import reverse
from django.contrib.auth.models import User
from bookings.models import Movie, Seat, Booking


@given('I am logged in as "{username}"')
def step_login_user(context, username):
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password('testpass123')
        user.save()
    context.user = user
    context.client.login(username=username, password='testpass123')


@when('I book seat "{seat_number}" for "{movie_title}"')
def step_book_seat(context, seat_number, movie_title):
    movie = Movie.objects.get(title=movie_title)
    seat = Seat.objects.get(seat_number=seat_number)
    context.response = context.client.post(
        reverse('book_seat', args=[movie.id]),
        {'seat_ids': [seat.id]}
    )


@then('I should be redirected to booking history')
def step_redirected_to_history(context):
    assert context.response.status_code == 302, \
        f'Expected 302, got {context.response.status_code}'
    assert reverse('booking_history') in context.response.url


@then('the booking should appear in my history')
def step_booking_in_history(context):
    response = context.client.get(reverse('booking_history'))
    assert context.movie.title in response.content.decode()


@given('seat "{seat_number}" is already booked for "{movie_title}"')
def step_prebook_seat(context, seat_number, movie_title):
    movie = Movie.objects.get(title=movie_title)
    seat = Seat.objects.get(seat_number=seat_number)
    booking = Booking.objects.create(movie=movie, user=context.user)
    booking.seats.set([seat])


@when('I try to book seat "{seat_number}" for "{movie_title}"')
def step_try_book_seat(context, seat_number, movie_title):
    movie = Movie.objects.get(title=movie_title)
    seat = Seat.objects.get(seat_number=seat_number)
    context.response = context.client.post(
        reverse('book_seat', args=[movie.id]),
        {'seat_ids': [seat.id]}
    )


@then('I should see an error about the seat being already booked')
def step_see_booking_error(context):
    content = context.response.content.decode()
    assert 'already booked' in content, \
        f'Expected "already booked" in response but not found'


@when('I visit the seat booking page for "{movie_title}" without logging in')
def step_visit_booking_unauth(context, movie_title):
    movie = Movie.objects.get(title=movie_title)
    context.response = context.client.get(reverse('book_seat', args=[movie.id]))


@then('I should be redirected to login')
def step_redirected_to_login(context):
    assert context.response.status_code == 302, \
        f'Expected 302, got {context.response.status_code}'
    assert 'login' in context.response.url
