# Development Notes - FlexOpt Selection System

**Note**: This system is designed to be completely reusable for any selection scenario (electives, training, courses, events, etc.). See CONFIGURATION.md for customization examples.

## Quick Start for Different Scenarios

### For Open Electives

```bash
# Configure for electives
# Update SITE_CONFIG in settings.py (see CONFIGURATION.md)
python manage.py populate_data electives
```

### For Training Programs

```bash
# Configure for training
# Update SITE_CONFIG in settings.py
python manage.py populate_data training
```

### For Course Selection

```bash
# Configure for courses
# Update SITE_CONFIG in settings.py
python manage.py populate_data courses
```

## WebSocket Development

The application includes real-time features using Django Channels and WebSockets. Here are the development options:

### Option 1: Standard Django Development Server (HTTP only)

```bash
# Use the standard startup script
./start.sh
# or
python manage.py runserver
```

-   ✅ Works for basic functionality
-   ✅ All forms and CRUD operations work
-   ❌ WebSocket connections will fail (expected)
-   📝 Use this for basic development and testing

### Option 2: ASGI Development Server (with WebSockets)

```bash
# Use the WebSocket-enabled startup script
./start_websocket.sh
# or
daphne -b 0.0.0.0 -p 8000 flex_opt.asgi:application
```

-   ✅ Full WebSocket support
-   ✅ Real-time subject count updates
-   ✅ Live quiz interactions
-   📝 Use this for complete feature testing

## Application Features Test Plan

### 1. Student Authentication & Dashboard

-   [x] Student login with email/password
-   [x] Dashboard showing assigned quizzes
-   [x] Previous submissions display
-   [x] Logout functionality

### 2. Quiz Interface

-   [x] Quiz detail page with subjects
-   [x] Subject selection interface
-   [x] Form validation and submission
-   [x] Redirect after submission
-   [x] Prevention of multiple submissions

### 3. Real-time Features (WebSocket required)

-   [x] Live subject availability counts
-   [x] Automatic disabling of full subjects
-   [x] Multi-user concurrent access
-   [x] WebSocket reconnection handling

### 4. Admin Interface

-   [x] Admin dashboard with statistics
-   [x] Quiz creation form
-   [x] Student assignment interface
-   [x] Results viewing and export
-   [x] Department/year/section filtering

### 5. Django Admin

-   [x] Model administration
-   [x] Custom admin interfaces
-   [x] Bulk operations
-   [x] Data validation

## Sample Test Scenarios

### Scenario 1: Basic Quiz Taking

1. Login as student: `alice.johnson@student.edu` / `password123`
2. Go to dashboard and click on available quiz
3. Select a subject and submit
4. Verify redirect to dashboard
5. Check that quiz no longer appears in available list

### Scenario 2: Real-time Updates (requires WebSocket server)

1. Open quiz page in two browser windows
2. Login as different students
3. Select subjects in one window
4. Observe live count updates in other window
5. Test subject becoming unavailable when full

### Scenario 3: Admin Management

1. Login to admin dashboard (staff user required)
2. Create a new quiz with selected subjects
3. Assign students using filters
4. View results and export data

## Database Structure

The application creates these main tables:

-   `elective_student` - Student information
-   `elective_subject` - Subject catalog
-   `elective_quiz` - Quiz definitions
-   `elective_studentquizresponse` - Student responses
-   Bridge tables for many-to-many relationships

## WebSocket Protocol

WebSocket connections use this format:

-   URL: `ws://localhost:8000/ws/quiz/<quiz_id>/`
-   Messages: JSON format with type and data fields
-   Authentication: Session-based through Django middleware

Example WebSocket message:

```json
{
	"type": "subject_update",
	"data": {
		"subject_id": 1,
		"current_count": 15,
		"is_full": false
	}
}
```

## Production Considerations

For production deployment:

1. Use Redis for channel layer instead of in-memory
2. Configure proper WebSocket load balancing
3. Set up SSL certificates for WSS connections
4. Use production ASGI server (Uvicorn/Hypercorn)
5. Configure static file serving

## Troubleshooting

### WebSocket Issues

-   Ensure using Daphne server for WebSocket support
-   Check browser console for connection errors
-   Verify WebSocket URL protocol (ws:// not https://)
-   Test with WebSocket debugging tools

### Database Issues

-   Reset with: `rm db.sqlite3 && python manage.py migrate`
-   Recreate sample data: `python manage.py populate_data`
-   Check admin interface for data verification

### Performance Issues

-   Monitor WebSocket connection count
-   Check channel layer memory usage
-   Optimize database queries for large datasets
-   Consider connection pooling for production
