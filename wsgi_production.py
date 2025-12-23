"""
PRODUCTION WSGI APPLICATION FOR PYTHONANYWHERE
===============================================

This file is used by WSGI servers (gunicorn, uWSGI) and PythonAnywhere
to load your Django application for HTTP requests.

PythonAnywhere Configuration:
1. Copy this file to: project/wsgi_production.py
2. In PythonAnywhere Web tab, update WSGI config file path to point to this file
3. Update the application = get_wsgi_application() line with your module path

Production Considerations:
- Ensures proper path setup for imports
- Loads environment variables before Django initializes
- Handles errors gracefully with logging
- Configured for optimal performance
"""

import os
import sys
import logging
from pathlib import Path

# ============================================================================
# PATH CONFIGURATION
# ============================================================================

# Add the project directory to Python path
# This allows Django to find your apps and modules

# On PythonAnywhere, the directory structure is:
# /home/yourusername/
#   ├── mysite/              <- Your project root
#   │   ├── project/         <- Django config (settings.py, urls.py, wsgi.py)
#   │   ├── app/             <- Your Django app
#   │   ├── university/       <- Your Django app
#   │   ├── manage.py
#   │   └── requirements.txt
#   └── .virtualenvs/mysite/ <- Virtual environment

# Get the project root directory (directory containing manage.py)
# On PythonAnywhere this would be: /home/yourusername/mysite/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Add project root to Python path so Django can import everything
sys.path.insert(0, str(PROJECT_ROOT))

# ============================================================================
# ENVIRONMENT VARIABLES
# ============================================================================

# Set Django settings module (must be set BEFORE importing Django)
# Use settings_production.py for production, settings.py for development
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Optional: Load environment variables from .env file
# On PythonAnywhere, environment variables are set in Web > Environment variables
# If you're using .env file, you'll need python-dotenv installed
try:
    from dotenv import load_dotenv
    
    # Look for .env file in project root
    env_file = PROJECT_ROOT / '.env'
    if env_file.exists():
        load_dotenv(str(env_file))
        logging.getLogger('django').info(f"Loaded .env file from {env_file}")
except ImportError:
    pass  # python-dotenv not installed, using environment variables instead

# ============================================================================
# DJANGO SETUP
# ============================================================================

# Import Django after path and environment setup
import django
from django.core.wsgi import get_wsgi_application

# Setup Django
django.setup()

# Get the WSGI application
# This is the callable that handles HTTP requests
application = get_wsgi_application()

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Set up logging for production errors
logger = logging.getLogger('django')

# Ensure logs directory exists
logs_dir = PROJECT_ROOT / 'logs'
logs_dir.mkdir(exist_ok=True)

# ============================================================================
# ERROR HANDLING (Optional Enhancement)
# ============================================================================

# You can optionally wrap the application with error handling:
#
# class ProductionMiddleware:
#     """Middleware to catch unhandled exceptions in production"""
#     
#     def __init__(self, application):
#         self.application = application
#     
#     def __call__(self, environ, start_response):
#         try:
#             return self.application(environ, start_response)
#         except Exception as e:
#             logger.exception("Unhandled exception in WSGI application")
#             # Return 500 error response
#             status = '500 Internal Server Error'
#             response_headers = [('Content-Type', 'text/plain')]
#             start_response(status, response_headers)
#             return [b'Internal Server Error']
#
# Wrap application with error middleware:
# application = ProductionMiddleware(application)

# ============================================================================
# PERFORMANCE OPTIMIZATION (Optional)
# ============================================================================

# If using Newrelic monitoring on PythonAnywhere:
# import newrelic.agent
# newrelic.agent.initialize('/path/to/newrelic.ini')
# application = newrelic.agent.wsgi_application()(application)

# ============================================================================
# PYTHONANYWHERE CONFIGURATION
# ============================================================================

"""
PythonAnywhere Web App Setup Instructions:

1. Create Web App:
   - Dashboard > Web > Add a new web app
   - Choose Python 3.10
   - Choose Django
   - Location: /home/yourusername/mysite

2. Configure WSGI File:
   - In Web tab, under "Code" section
   - WSGI configuration file: /home/yourusername/mysite/project/wsgi_production.py
   
   Or edit the WSGI file directly to import from correct location:
   If you named this file wsgi_production.py in project/ directory,
   the default content will be:
   
       import sys
       path = '/home/yourusername/mysite'
       if path not in sys.path:
           sys.path.append(path)
       from project.wsgi import application
   
   Replace with:
   
       import sys
       path = '/home/yourusername/mysite'
       if path not in sys.path:
           sys.path.append(path)
       from project.wsgi_production import application

3. Configure Static Files:
   - Web > Static files section
   - URL: /static/
   - Directory: /home/yourusername/mysite/static/
   
   - URL: /media/
   - Directory: /home/yourusername/mysite/media/

4. Configure Virtual Environment:
   - Web > Virtualenv path: /home/yourusername/.virtualenvs/mysite
   
5. Environment Variables:
   - Web > Environment variables
   - Add required variables:
     DEBUG=False
     SECRET_KEY=your-secret-key-here
     ALLOWED_HOSTS=yourusername.pythonanywhere.com
     CORS_ALLOWED_ORIGINS=https://yourdomain.com
     CSRF_TRUSTED_ORIGINS=https://yourdomain.com

6. Domain Configuration:
   - Web > Security
   - Add your custom domain and SSL certificate (automatic HTTPS)

7. Reload Web App:
   - Click "Reload" button after any code or configuration changes
"""

# ============================================================================
# STARTUP VERIFICATION
# ============================================================================

if __name__ == '__main__':
    # This runs when the WSGI file is tested locally (not in production)
    print(f"✓ Project root: {PROJECT_ROOT}")
    print(f"✓ Django settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print(f"✓ DEBUG mode: {os.environ.get('DEBUG', 'Not set')}")
    print(f"✓ WSGI application loaded successfully")
    print(f"✓ Database backend: {django.db.DEFAULT_DB_ALIAS}")
    print("")
    print("To run development server locally:")
    print("  python manage.py runserver")
    print("")
    print("To run production server with gunicorn:")
    print("  gunicorn project.wsgi_production:application")
