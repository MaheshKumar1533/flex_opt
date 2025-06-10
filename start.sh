#!/bin/bash

# Open Elective Selection System - Startup Script

echo "🎓 Open Elective Selection System"
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run installation first."
    echo "Run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if database exists
if [ ! -f "db.sqlite3" ]; then
    echo "📦 Setting up database..."
    python manage.py migrate
    echo "📊 Creating sample data..."
    python manage.py populate_data
fi

echo "🚀 Starting development server..."
echo ""
echo "📱 Access the application at:"
echo "   Student Login: http://localhost:8000/"
echo "   Admin Dashboard: http://localhost:8000/admin-dashboard/"
echo "   Django Admin: http://localhost:8000/admin/"
echo ""
echo "👥 Sample Credentials:"
echo "   Student: alice.johnson@student.edu / password123"
echo "   Admin: admin / admin123"
echo ""
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
