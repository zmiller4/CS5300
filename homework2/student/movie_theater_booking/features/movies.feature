Feature: Movie Listings
    As a visitor
    I want to see available movies
    So that I can choose a movie to watch

    Scenario: View movie listings page
        Given a movie "Interstellar" exists
        When I visit the movie list page
        Then I should see "Interstellar" on the page
        And the page should load successfully

    Scenario: View empty movie listings
        Given no movies exist
        When I visit the movie list page
        Then I should see "No movies available" on the page

    Scenario: View movie details via API
        Given a movie "Interstellar" exists
        And I am an authenticated API user
        When I request the movie list from the API
        Then the API should return 1 movie
        And the movie title should be "Interstellar"
