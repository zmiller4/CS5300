# Movie Theater Booking Application

A RESTful Movie Theater Booking Application built with Python, Django, and Django REST Framework.

## Project Structure

```
movie_theater_booking/
├── manage.py
├── requirements.txt
├── movie_theater_booking/       # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── bookings/                    # Main application
    ├── models.py                # Movie, Seat, Booking models
    ├── serializers.py           # DRF serializers
    ├── views.py                 # ViewSets and template views
    ├── urls.py                  # URL routing (API + templates)
    ├── admin.py                 # Admin configuration
    ├── tests.py                 # Unit and integration tests
    └── templates/bookings/      # HTML templates
        ├── base.html            # Base template with Bootstrap
        ├── movie_list.html      # Movie listings
        ├── seat_booking.html    # Seat selection and booking
        ├── booking_history.html # User booking history
        ├── login.html           # Login page
        └── register.html        # Registration page
```

## Setup and Installation

### Prerequisites
- Python 3.10+
- pip

### Local Setup

1. **Clone the repository** and navigate to the project directory:
   ```bash
   cd movie_theater_booking
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv myenv
   source myenv/bin/activate   # Linux/Mac
   myenv\Scripts\activate      # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Web UI: http://127.0.0.1:8000/
   - API Root: http://127.0.0.1:8000/api/
   - Admin Panel: http://127.0.0.1:8000/admin/

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/movies/` | GET | List all movies |
| `/api/movies/` | POST | Create a new movie |
| `/api/movies/<id>/` | GET | Retrieve a movie |
| `/api/movies/<id>/` | PUT | Update a movie |
| `/api/movies/<id>/` | DELETE | Delete a movie |
| `/api/seats/` | GET | List all seats (check availability) |
| `/api/seats/` | POST | Create a new seat |
| `/api/seats/<id>/` | GET | Retrieve a seat |
| `/api/bookings/` | GET | List all bookings |
| `/api/bookings/` | POST | Create a new booking |
| `/api/bookings/<id>/` | GET | Retrieve a booking |

## Running Tests

### Unit and Integration Tests

```bash
python manage.py test bookings
```

### BDD Tests (Behave)

```bash
python manage.py behave
```

### Test Coverage

```bash
coverage run manage.py test bookings
coverage report
```

## Features

- **Movie Listings**: Browse available movies with details (title, description, release date, duration).
- **Seat Booking**: Select and book available seats for a movie.
- **Booking History**: View personal booking history.
- **User Authentication**: Register, login, and logout.
- **RESTful API**: Full CRUD operations on movies, seats, and bookings via Django REST Framework.
- **Responsive UI**: Bootstrap-based dark-themed interface.

## Technologies Used

- **Backend**: Django 4.2, Django REST Framework
- **Frontend**: Bootstrap 5.3, Django Templates
- **Database**: SQLite (development)
- **Deployment**: Render with Gunicorn and WhiteNoise

## Deployment

This application is deployed on Render. The deployment configuration includes:

- `Procfile` - Gunicorn web server configuration
- `build.sh` - Build script for installing dependencies, collecting static files, and running migrations
- `runtime.txt` - Python version specification
- `whitenoise` - Static file serving in production

### Render Environment Variables

Set the following environment variables in Render:

| Variable | Description |
|---|---|
| `SECRET_KEY` | A secure random secret key |
| `DEBUG` | Set to `False` for production |
| `ALLOWED_HOSTS` | Your Render domain (e.g., `your-app.onrender.com`) |

## AI Usage Citation

This project utilized AI assistance (Claude by Anthropic) in the following ways:

- **Code generation**: AI was used to help generate boilerplate code for Django models, serializers, views, and URL routing.
- **Test writing**: AI assisted in writing unit tests, integration tests, and Behave BDD test scenarios.
- **UI development**: AI helped create Bootstrap-styled templates with a retro-futuristic design theme.
- **Debugging**: AI was used to troubleshoot errors during development.
- **Documentation**: AI assisted in writing this README and code comments.

All AI-generated content was directed, reviewed, tested, and adapted to fit the project requirements by Zach Miller.
