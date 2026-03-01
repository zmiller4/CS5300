from behave import given, when, then
from django.urls import reverse
from django.contrib.auth.models import User


@when('I register with username "{username}" and password "{password}"')
def step_register(context, username, password):
    context.response = context.client.post(reverse('register'), {
        'username': username,
        'password1': password,
        'password2': password,
    })


@then('I should be redirected to the movie list')
def step_redirected_to_movies(context):
    assert context.response.status_code == 302, \
        f'Expected 302, got {context.response.status_code}'
    assert reverse('movie_list') in context.response.url


@then('the user "{username}" should exist')
def step_user_exists(context, username):
    assert User.objects.filter(username=username).exists()


@given('a user "{username}" with password "{password}" exists')
def step_create_user(context, username, password):
    User.objects.create_user(username=username, password=password)


@when('I login with username "{username}" and password "{password}"')
def step_login(context, username, password):
    context.response = context.client.post(reverse('login'), {
        'username': username,
        'password': password,
    })


@then('I should stay on the login page')
def step_stay_on_login(context):
    assert context.response.status_code == 200, \
        f'Expected 200, got {context.response.status_code}'


@when('I logout')
def step_logout(context):
    context.response = context.client.get(reverse('logout'))
