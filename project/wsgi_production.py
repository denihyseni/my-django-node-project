"""
Production-Ready WSGI Configuration for PythonAnywhere
Django 4.2.7 + Python 3.10 Optimized

This WSGI file is configured for:
- PythonAnywhere deployment
- Environment variable loading
- Proper path setup
- Error handling
"""

import os
import sys
from pathlib import Path

# ============================================================================
# PATH SETUP - CRITICAL FOR PYTHONANYWHERE
# ============================================================================

# Get the directory of this file
this_file = Path(__file__)
project_dir = this_file.parent  # /home/yourusername/university-portal/project
base_dir = project_dir.parent    # /home/yourusername/university-portal

# Add project to Python path
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_file = os.path.join(base_dir, '.env')
    if os.path.exists(env_file):
        load_dotenv(env_file)
except ImportError:
    # python-dotenv not available, environment vars must be set manually
    pass

# ============================================================================
# DJANGO SETUP
# ============================================================================

from django.core.wsgi import get_wsgi_application

# Initialize Django
application = get_wsgi_application()

# ============================================================================
# ERROR LOGGING
# ============================================================================

import logging

logger = logging.getLogger(__name__)

# Log successful WSGI initialization
try:
    from django.conf import settings
    logger.info(
        f"Django WSGI initialized | DEBUG={settings.DEBUG} | "
        f"ALLOWED_HOSTS={settings.ALLOWED_HOSTS}"
    )
except Exception as e:
    logger.error(f"Error during WSGI initialization: {e}")

# ============================================================================
# PYTHONANYWHERE CONFIGURATION NOTES
# ============================================================================

"""
WSGI FILE SETUP FOR PYTHONANYWHERE:

1. In PythonAnywhere Web app configuration:
   - Go to "Web" section
   - Click your web app
   - Under "Code" section, you'll see WSGI configuration file path
   - It should point to: /home/yourusername/university-portal/project/project/wsgi.py
   
2. The WSGI file location in PythonAnywhere:
   - Default path: /var/www/yourusername_pythonanywhere_com_wsgi.py
   - Custom path: /home/yourusername/university-portal/project/project/wsgi.py
   
3. Edit the web app configuration:
   - Source code: /home/yourusername/university-portal
   - Working directory: /home/yourusername/university-portal
   - WSGI configuration file: /home/yourusername/university-portal/project/project/wsgi.py

4. Environment Variables (set in Web app security):
   - SECRET_KEY (important: unique for production)
   - DEBUG=False
   - ALLOWED_HOSTS=yourusername.pythonanywhere.com
   - CORS_ALLOWED_ORIGINS=https://yourusername.pythonanywhere.com
   - CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com

5. After updating:
   - Click "Reload" button in Web app
   - Check error log if issues: /var/log/yourusername.pythonanywhere.com.error.log
"""
