Feature: User Authentication
    As a visitor
    I want to register, login, and logout
    So that I can use the booking system

    Scenario: Register a new user
        When I register with username "newuser" and password "ComplexPass123!"
        Then I should be redirected to the movie list
        And the user "newuser" should exist

    Scenario: Login with valid credentials
        Given a user "existinguser" with password "ComplexPass123!" exists
        When I login with username "existinguser" and password "ComplexPass123!"
        Then I should be redirected to the movie list

    Scenario: Login with invalid credentials
        When I login with username "nobody" and password "wrongpass"
        Then I should stay on the login page

    Scenario: Logout redirects to movie list
        Given a user "logoutuser" with password "ComplexPass123!" exists
        And I am logged in as "logoutuser"
        When I logout
        Then I should be redirected to the movie list
