"""
WSGI config for genai_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')

# Create WSGI application
application = get_wsgi_application()

# For Elastic Beanstalk health checks
def application_health_check(environ, start_response):
    """Simple health check endpoint for load balancer"""
    if environ.get('PATH_INFO') == '/health':
        status = '200 OK'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'OK']
    return application(environ, start_response)