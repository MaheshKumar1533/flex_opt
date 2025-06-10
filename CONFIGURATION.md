# FlexOpt Configuration Examples

This file contains configuration examples for different use cases of the FlexOpt Selection System.

## How to Configure

Update the `SITE_CONFIG` dictionary in `flex_opt/settings.py` to customize the application for your specific use case.

## Example Configurations

### 1. Open Elective Selection (University)

```python
SITE_CONFIG = {
    'SITE_NAME': 'Open Elective Selection System',
    'SITE_DESCRIPTION': 'Select your preferred open elective subject for the semester. Limited seats available!',
    'SITE_LOGO_TEXT': 'Electives Portal',
    'DEFAULT_QUIZ_TYPE': 'Elective Selection',
    'DEFAULT_SUBJECT_TYPE': 'Elective Subject',
}
```

### 2. Corporate Training Programs

```python
SITE_CONFIG = {
    'SITE_NAME': 'Training Program Selection',
    'SITE_DESCRIPTION': 'Choose your professional development training program. Register now!',
    'SITE_LOGO_TEXT': 'Training Hub',
    'DEFAULT_QUIZ_TYPE': 'Training Selection',
    'DEFAULT_SUBJECT_TYPE': 'Training Program',
}
```

### 3. Course Selection System

```python
SITE_CONFIG = {
    'SITE_NAME': 'Course Enrollment System',
    'SITE_DESCRIPTION': 'Register for advanced courses. Early bird selection available.',
    'SITE_LOGO_TEXT': 'CourseSelect',
    'DEFAULT_QUIZ_TYPE': 'Course Registration',
    'DEFAULT_SUBJECT_TYPE': 'Course',
}
```

### 4. Workshop/Event Registration

```python
SITE_CONFIG = {
    'SITE_NAME': 'Workshop Registration Portal',
    'SITE_DESCRIPTION': 'Register for technical workshops and seminars. Limited capacity!',
    'SITE_LOGO_TEXT': 'WorkshopHub',
    'DEFAULT_QUIZ_TYPE': 'Workshop Registration',
    'DEFAULT_SUBJECT_TYPE': 'Workshop',
}
```

### 5. Resource Allocation System

```python
SITE_CONFIG = {
    'SITE_NAME': 'Resource Allocation System',
    'SITE_DESCRIPTION': 'Book your preferred resources and facilities.',
    'SITE_LOGO_TEXT': 'ResourceBook',
    'DEFAULT_QUIZ_TYPE': 'Resource Booking',
    'DEFAULT_SUBJECT_TYPE': 'Resource',
}
```

### 6. Project Assignment System

```python
SITE_CONFIG = {
    'SITE_NAME': 'Project Assignment Portal',
    'SITE_DESCRIPTION': 'Choose your project assignments for the semester.',
    'SITE_LOGO_TEXT': 'ProjectSelect',
    'DEFAULT_QUIZ_TYPE': 'Project Assignment',
    'DEFAULT_SUBJECT_TYPE': 'Project',
}
```

## Deployment Notes

1. **No Code Changes Required**: Simply update the configuration and restart the application
2. **Database Compatibility**: All configurations use the same database schema
3. **Sample Data**: Use the populate_data command with different scenarios:
    - `python manage.py populate_data electives`
    - `python manage.py populate_data training`
    - `python manage.py populate_data courses`
    - `python manage.py populate_data all`

## Advanced Customization

For deeper customization, you can also:

1. **Custom CSS**: Modify `static/css/custom.css` for branding
2. **Logo Images**: Add logo images and update the navbar in `base.html`
3. **Email Templates**: Customize notification templates
4. **Additional Fields**: Extend models for specific requirements

The system is designed to be completely white-label and adaptable to any selection-based scenario!
