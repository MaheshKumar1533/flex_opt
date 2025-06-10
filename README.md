# FlexOpt Selection System

A comprehensive Django web application for managing dynamic selection processes using quizzes with real-time updates via WebSockets. **Fully reusable for any scenario:** open electives, training programs, course selection, or any other selection-based system.

## Features

### 🎯 Core Functionality

-   **Student Management**: Student registration with department, year, and section filtering
-   **Dynamic Subject Management**: Subjects/courses/programs with capacity limits
-   **Flexible Quiz System**: Create quizzes for any selection scenario
-   **Real-time Updates**: Live subject availability counts using Django Channels and WebSockets
-   **Single Selection**: Each student can select only one subject per quiz
-   **Capacity Management**: Subjects automatically become unavailable when full
-   **Multi-scenario Support**: Works for electives, training, courses, events, etc.

### 🔧 Technical Features

-   **Django Framework**: Robust backend with SQLite database
-   **Django Channels**: Real-time WebSocket communication
-   **Bootstrap UI**: Modern, responsive user interface
-   **Admin Interface**: Comprehensive admin panel for management
-   **RESTful APIs**: Django REST Framework integration
-   **Security**: Password hashing and session management

## 🚀 Quick Setup for Different Scenarios

### Option 1: Use the Configuration Helper (Recommended)

```bash
./configure.sh
```

This interactive script will configure the system for your use case and populate sample data.

### Option 2: Manual Configuration

1. **Edit Configuration**: Update `SITE_CONFIG` in `flex_opt/settings.py` (see examples in `CONFIGURATION.md`)
2. **Apply Migrations**: `python manage.py migrate`
3. **Load Sample Data**: `python manage.py populate_data [scenario]`
    - `electives` - University elective selection
    - `training` - Corporate training programs
    - `courses` - Advanced course selection
    - `all` - All scenarios for testing
4. **Create Admin**: `python manage.py createsuperuser`
5. **Start Server**: `./start.sh`

### Example: Configure for Training Programs

```python
# In flex_opt/settings.py
SITE_CONFIG = {
    'SITE_NAME': 'Training Program Selection',
    'SITE_DESCRIPTION': 'Choose your professional development training program.',
    'SITE_LOGO_TEXT': 'Training Hub',
    'DEFAULT_QUIZ_TYPE': 'Training Selection',
    'DEFAULT_SUBJECT_TYPE': 'Training Program',
}
```

Then run:

```bash
python manage.py populate_data training
./start.sh
```

## Installation

### Prerequisites

-   Python 3.8+
-   pip
-   Git

### Setup Instructions

1. **Clone the repository**

    ```bash
    cd /path/to/your/projects
    git clone <repository-url>  # or extract the project files
    cd flex_opt
    ```

2. **Create and activate virtual environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run database migrations**

    ```bash
    python manage.py migrate
    ```

5. **Create sample data (optional)**

    ```bash
    python manage.py populate_data
    ```

6. **Create superuser for admin access**

    ```bash
    python manage.py createsuperuser
    ```

7. **Start the development server**

    ```bash
    python manage.py runserver
    ```

8. **Access the application**
    - Student Interface: http://localhost:8000/
    - Admin Interface: http://localhost:8000/admin-dashboard/
    - Django Admin: http://localhost:8000/admin/

## Usage

### For Students

1. **Login**

    - Go to http://localhost:8000/
    - Use your email and password to log in
    - Sample credentials: `alice.johnson@student.edu` / `password123`

2. **Dashboard**

    - View available quizzes assigned to you
    - See your previous submissions
    - Access active quizzes

3. **Taking a Quiz**
    - Click on an available quiz
    - View all subjects with real-time availability
    - Select your preferred subject
    - Confirm your selection (cannot be changed)

### For Administrators

1. **Admin Dashboard**

    - Login as staff user
    - Access at http://localhost:8000/admin-dashboard/
    - View system statistics

2. **Creating Quizzes**

    - Click "Create New Quiz"
    - Set title, description, and schedule
    - Select subjects to include
    - Save the quiz

3. **Assigning Students**

    - Select a quiz and click "Assign Students"
    - Filter by department, year, or section
    - Select individual students or use bulk assignment
    - Save assignments

4. **Viewing Results**
    - Click on "Results" for any quiz
    - View subject-wise distribution
    - Export results as CSV
    - See detailed student responses

### Django Admin Interface

1. **Access**: http://localhost:8000/admin/
2. **Login**: Use superuser credentials
3. **Features**:
    - Manage students, subjects, quizzes
    - View and edit all data
    - User management
    - System administration

## 🔄 Reusability

The system is completely reusable for different scenarios:

-   **Models**: Generic enough to handle any selection scenario
-   **Student**: Can represent learners, employees, participants, etc.
-   **Subject**: Can represent courses, programs, workshops, resources, etc.
-   **Quiz**: Can represent selection events, registrations, assignments, etc.
-   **Views**: Dynamic terminology based on configuration
-   **Templates**: Use configurable text and labels
-   **Admin**: Generic interface works for any content type

Simply update `SITE_CONFIG` in settings.py to rebrand for your use case!

## Models

### Student

-   Name, Roll Number, Email, Password
-   Department, Year, Section
-   Related quiz responses

### Subject

-   Name, Code, Description
-   Maximum limit and current count
-   Availability status

### Quiz

-   Title, Description, Schedule
-   Associated subjects
-   Assigned students
-   Activity status

### StudentQuizResponse

-   Links student to quiz and selected subject
-   Timestamp tracking
-   Unique constraint (one response per student per quiz)

## Real-time Features

The application uses Django Channels for WebSocket communication:

-   **Live Updates**: Subject availability updates in real-time
-   **Instant Feedback**: See when subjects become full
-   **Concurrent Access**: Multiple students can access simultaneously
-   **Automatic Reconnection**: WebSocket auto-reconnects on connection loss

## API Endpoints

### Student Interface

-   `GET /` - Home page (redirects to login or dashboard)
-   `POST /login/` - Student login
-   `GET /dashboard/` - Student dashboard
-   `GET /quiz/<id>/` - Quiz detail page
-   `POST /quiz/<id>/submit/` - Submit quiz response

### Admin Interface

-   `GET /admin-dashboard/` - Admin dashboard
-   `GET /admin/create-quiz/` - Create quiz form
-   `POST /admin/create-quiz/` - Create quiz submission
-   `GET /admin/quiz/<id>/assign/` - Assign students page
-   `GET /admin/quiz/<id>/results/` - Quiz results page

### WebSocket

-   `ws://localhost:8000/ws/quiz/<quiz_id>/` - Real-time quiz updates

## Configuration

### Settings (flex_opt/settings.py)

-   Database: SQLite (development)
-   Channels: In-memory layer (development)
-   Static files: Bootstrap CDN + custom CSS
-   Debug mode: Enabled for development

### WebSocket Configuration

The system uses Django Channels with:

-   ASGI application setup
-   In-memory channel layer (development)
-   Authentication middleware for WebSockets

## Sample Data

The `populate_data` management command creates:

-   6 sample subjects (CS501-CS506)
-   15 sample students across different departments
-   1 active quiz with assignments
-   Default passwords: `password123` for all students

## Development

### Project Structure

```
flex_opt/
├── manage.py
├── requirements.txt
├── flex_opt/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── elective/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── consumers.py
│   ├── routing.py
│   ├── templates/
│   └── management/
└── static/
    └── css/
```

### Adding New Features

1. Create models in `elective/models.py`
2. Run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Add views in `elective/views.py`
4. Create templates in `elective/templates/elective/`
5. Update URLs in `elective/urls.py`

### WebSocket Development

-   Consumers are in `elective/consumers.py`
-   Routing defined in `elective/routing.py`
-   Client-side WebSocket code in templates

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**

    - Check if Channels is installed: `pip install channels`
    - Verify ASGI configuration in settings
    - Ensure WebSocket URL is correct

2. **Database Migration Errors**

    - Delete `db.sqlite3` and migration files (except `__init__.py`)
    - Run `python manage.py makemigrations elective`
    - Run `python manage.py migrate`

3. **Static Files Not Loading**

    - Check `STATIC_URL` and `STATICFILES_DIRS` in settings
    - Run `python manage.py collectstatic` for production
    - Ensure Bootstrap CDN is accessible

4. **Permission Errors**
    - Verify user is staff for admin access
    - Check session authentication for students
    - Ensure correct login credentials

### Development Server

-   Use `python manage.py runserver 0.0.0.0:8000` for network access
-   Enable debug mode for detailed error messages
-   Check console for WebSocket connection status

## Production Deployment

For production deployment:

1. **Database**: Switch to PostgreSQL/MySQL
2. **WebSocket**: Use Redis channel layer
3. **Static Files**: Configure proper static file serving
4. **Security**: Update SECRET_KEY, disable DEBUG
5. **Web Server**: Use Gunicorn/uWSGI with Nginx
6. **WebSocket Server**: Use Daphne for ASGI

### Production Settings Example

```python
# Channel layer with Redis
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

# PostgreSQL Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'flex_opt_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🎯 Reusability & Dynamic Configuration

**FlexOpt is designed to be completely reusable for different scenarios:**

### Pre-configured Use Cases

-   **Open Electives**: Traditional university elective selection
-   **Training Programs**: Corporate/professional training selection
-   **Course Selection**: Academic course enrollment
-   **Event Registration**: Workshop/seminar selection
-   **Resource Allocation**: Any first-come-first-served resource assignment

### Dynamic Configuration

The system can be easily customized by modifying the `SITE_CONFIG` in `settings.py`:

```python
SITE_CONFIG = {
    'SITE_NAME': 'Training Program Selection',           # Customize site name
    'SITE_DESCRIPTION': 'Select your training program', # Login page description
    'SITE_LOGO_TEXT': 'Training Portal',               # Navigation logo text
    'DEFAULT_QUIZ_TYPE': 'Training Selection',          # Default quiz type
    'DEFAULT_SUBJECT_TYPE': 'Training Program',         # Subject terminology
}
```

**No code changes required** - just update the configuration and the entire UI adapts!

## License

This project is developed for educational purposes. Feel free to modify and use for your requirements.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review Django and Channels documentation
3. Check browser console for WebSocket errors
4. Verify database integrity with Django admin
