#!/bin/bash

# Open Elective Selection System - WebSocket Development Server

echo "🎓 Open Elective Selection System (with WebSocket Support)"
echo "========================================================="

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

echo "🚀 Starting ASGI development server with WebSocket support..."
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
echo "⚡ WebSocket URL: ws://localhost:8000/ws/quiz/<quiz_id>/"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Set Django settings module
export DJANGO_SETTINGS_MODULE=flex_opt.settings

# Use Daphne for ASGI (WebSocket support)
daphne -b 0.0.0.0 -p 8000 flex_opt.asgi:application
