from behave import given, when, then
from django.urls import reverse
from bookings.models import Movie
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from datetime import date


@given('a movie "{title}" exists')
def step_create_movie(context, title):
    context.movie = Movie.objects.create(
        title=title,
        description=f'A great movie called {title}.',
        release_date=date(2025, 6, 15),
        duration=120
    )


@given('no movies exist')
def step_no_movies(context):
    Movie.objects.all().delete()


@when('I visit the movie list page')
def step_visit_movie_list(context):
    context.response = context.client.get(reverse('movie_list'))


@then('I should see "{text}" on the page')
def step_see_text(context, text):
    content = context.response.content.decode()
    assert text in content, f'Expected "{text}" in response but not found'


@then('the page should load successfully')
def step_page_loads(context):
    assert context.response.status_code == 200


@given('I am an authenticated API user')
def step_create_and_auth_api_user(context):
    user = User.objects.create_user(username='apiuser', password='testpass123')
    context.api_client = APIClient()
    context.api_client.force_authenticate(user=user)


@when('I request the movie list from the API')
def step_api_movie_list(context):
    context.api_response = context.api_client.get(reverse('movie-list'))


@then('the API should return {count:d} movie')
def step_api_count(context, count):
    assert len(context.api_response.data) == count, \
        f'Expected {count} movies, got {len(context.api_response.data)}'


@then('the movie title should be "{title}"')
def step_api_movie_title(context, title):
    assert context.api_response.data[0]['title'] == title
