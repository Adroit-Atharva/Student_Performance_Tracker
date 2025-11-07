#!/bin/bash

# Create main project directory
mkdir -p student_course_tracker
cd student_course_tracker || exit

# Core folders
mkdir -p app/{models,controllers,views,utils}
mkdir -p data
mkdir -p tests

# Key files
touch app/__init__.py
touch app/main.py
touch app/models/__init__.py
touch app/controllers/__init__.py
touch app/views/__init__.py
touch app/utils/__init__.py
touch requirements.txt
touch README.md

# Optional: sample placeholders
echo "# Student Course and Performance Tracker" > README.md
echo "psycopg2" > requirements.txt

# Print success message
echo "✅ Project structure created successfully!"
tree -L 3

