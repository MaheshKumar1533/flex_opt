#!/bin/bash

# FlexOpt Configuration Helper
# This script helps configure the application for different use cases

echo "FlexOpt Selection System - Configuration Helper"
echo "=============================================="
echo
echo "This script will help you configure FlexOpt for your specific use case."
echo
echo "Available configurations:"
echo "1. Open Elective Selection (University)"
echo "2. Corporate Training Programs"
echo "3. Course Selection System"
echo "4. Workshop/Event Registration"
echo "5. Resource Allocation System"
echo "6. Custom Configuration"
echo

read -p "Select configuration (1-6): " choice

case $choice in
    1)
        echo "Configuring for Open Elective Selection..."
        CONFIG_NAME="Open Elective Selection System"
        CONFIG_DESC="Select your preferred open elective subject for the semester. Limited seats available!"
        CONFIG_LOGO="Electives Portal"
        CONFIG_QUIZ="Elective Selection"
        CONFIG_SUBJECT="Elective Subject"
        SAMPLE_DATA="electives"
        ;;
    2)
        echo "Configuring for Corporate Training Programs..."
        CONFIG_NAME="Training Program Selection"
        CONFIG_DESC="Choose your professional development training program. Register now!"
        CONFIG_LOGO="Training Hub"
        CONFIG_QUIZ="Training Selection"
        CONFIG_SUBJECT="Training Program"
        SAMPLE_DATA="training"
        ;;
    3)
        echo "Configuring for Course Selection..."
        CONFIG_NAME="Course Enrollment System"
        CONFIG_DESC="Register for advanced courses. Early bird selection available."
        CONFIG_LOGO="CourseSelect"
        CONFIG_QUIZ="Course Registration"
        CONFIG_SUBJECT="Course"
        SAMPLE_DATA="courses"
        ;;
    4)
        echo "Configuring for Workshop/Event Registration..."
        CONFIG_NAME="Workshop Registration Portal"
        CONFIG_DESC="Register for technical workshops and seminars. Limited capacity!"
        CONFIG_LOGO="WorkshopHub"
        CONFIG_QUIZ="Workshop Registration"
        CONFIG_SUBJECT="Workshop"
        SAMPLE_DATA="all"
        ;;
    5)
        echo "Configuring for Resource Allocation..."
        CONFIG_NAME="Resource Allocation System"
        CONFIG_DESC="Book your preferred resources and facilities."
        CONFIG_LOGO="ResourceBook"
        CONFIG_QUIZ="Resource Booking"
        CONFIG_SUBJECT="Resource"
        SAMPLE_DATA="all"
        ;;
    6)
        echo "Custom Configuration..."
        read -p "Site Name: " CONFIG_NAME
        read -p "Site Description: " CONFIG_DESC
        read -p "Logo Text: " CONFIG_LOGO
        read -p "Quiz Type: " CONFIG_QUIZ
        read -p "Subject Type: " CONFIG_SUBJECT
        read -p "Sample Data (electives/training/courses/all): " SAMPLE_DATA
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo
echo "Configuration Summary:"
echo "====================="
echo "Site Name: $CONFIG_NAME"
echo "Description: $CONFIG_DESC"
echo "Logo Text: $CONFIG_LOGO"
echo "Quiz Type: $CONFIG_QUIZ"
echo "Subject Type: $CONFIG_SUBJECT"
echo "Sample Data: $SAMPLE_DATA"
echo

read -p "Apply this configuration? (y/N): " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    echo
    echo "Applying configuration..."

    # Backup current settings
    cp flex_opt/settings.py flex_opt/settings.py.backup

    # Update SITE_CONFIG in settings.py
    cat > temp_config.py << EOF
# Auto-generated configuration
SITE_CONFIG = {
    'SITE_NAME': '$CONFIG_NAME',
    'SITE_DESCRIPTION': '$CONFIG_DESC',
    'SITE_LOGO_TEXT': '$CONFIG_LOGO',
    'DEFAULT_QUIZ_TYPE': '$CONFIG_QUIZ',
    'DEFAULT_SUBJECT_TYPE': '$CONFIG_SUBJECT',
}
EOF

    # Replace the SITE_CONFIG section
    python3 << 'PYTHON_SCRIPT'
import re

# Read current settings
with open('flex_opt/settings.py', 'r') as f:
    content = f.read()

# Read new config
with open('temp_config.py', 'r') as f:
    new_config = f.read()

# Replace SITE_CONFIG section
pattern = r'SITE_CONFIG = \{[^}]*\}'
replacement = new_config.split('= ')[1].strip()
replacement = f'SITE_CONFIG = {replacement}'

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open('flex_opt/settings.py', 'w') as f:
    f.write(content)

print("Settings updated successfully!")
PYTHON_SCRIPT

    # Clean up temp file
    rm temp_config.py

    echo "Configuration applied successfully!"
    echo
    echo "Next steps:"
    echo "1. Run migrations: python manage.py migrate"
    echo "2. Load sample data: python manage.py populate_data $SAMPLE_DATA"
    echo "3. Create superuser: python manage.py createsuperuser"
    echo "4. Start server: ./start.sh"
    echo
    echo "Your FlexOpt system is now configured for: $CONFIG_NAME"

else
    echo "Configuration cancelled."
fi
