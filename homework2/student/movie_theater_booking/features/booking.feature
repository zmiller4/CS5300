Feature: Seat Booking
    As a registered user
    I want to book seats for a movie
    So that I can watch the movie at the theater

    Scenario: Book a seat for a movie
        Given a movie "Dune" exists
        And I am logged in as "testuser"
        When I book seat "A1" for "Dune"
        Then I should be redirected to booking history
        And the booking should appear in my history

    Scenario: Cannot book an already booked seat
        Given a movie "Dune" exists
        And I am logged in as "testuser"
        And seat "A1" is already booked for "Dune"
        When I try to book seat "A1" for "Dune"
        Then I should see an error about the seat being already booked

    Scenario: Booking requires login
        Given a movie "Avatar" exists
        When I visit the seat booking page for "Avatar" without logging in
        Then I should be redirected to login
