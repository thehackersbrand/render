# Development Environment Guide

This Django GenAI application has been configured specifically for development environment.

## What Was Changed

### Removed Production Components
- ✅ Removed AWS Elastic Beanstalk configuration files (.ebextensions/, .elasticbeanstalk/)
- ✅ Removed deployment scripts (deploy.bat, deploy.sh)
- ✅ Removed production dependencies (gunicorn, whitenoise, PyMySQL)
- ✅ Removed AWS deployment guides and troubleshooting docs
- ✅ Removed production security settings
- ✅ Removed MySQL/RDS database configuration

### Development Optimizations
- ✅ Simplified settings.py for development only
- ✅ DEBUG=True always enabled
- ✅ SQLite database configuration only
- ✅ Development-friendly ALLOWED_HOSTS
- ✅ Removed WhiteNoise middleware
- ✅ Console email backend for development
- ✅ Updated .env file with development defaults

## Quick Start

1. **Activate virtual environment:**
   ```cmd
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Update Euron API key in .env file**

4. **Run migrations:**
   ```cmd
   python manage.py migrate
   ```

5. **Start development server:**
   ```cmd
   python manage.py runserver
   ```

## Development Features

- **SQLite Database**: Simple file-based database (db.sqlite3)
- **Debug Mode**: Always enabled with detailed error pages
- **Static Files**: Served by Django development server
- **Hot Reload**: Server automatically restarts on code changes
- **Console Email**: Email sent to console for testing
- **Admin Interface**: Available at `/admin/`

## File Structure (Development)

```
├── accounts/               # User authentication app
├── chat/                  # AI chat functionality
├── genai_project/         # Django project settings
├── static/                # Static files (CSS, JS, Images)
├── staticfiles/           # Collected static files
├── templates/             # HTML templates
├── .env                   # Environment variables
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Development Best Practices

1. **Always use virtual environment**
2. **Keep .env file secure (not in version control)**
3. **Use SQLite for local development**
4. **Test API connectivity with test_euron_api.py**
5. **Use Django admin for user management**
6. **Check Django debug toolbar for performance**

## Common Development Commands

```cmd
# Start development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (if needed)
python manage.py collectstatic

# Django shell
python manage.py shell

# Run tests
python manage.py test
```

## Environment Variables (.env)

```env
SECRET_KEY=django-insecure-dev-key-only-for-development-change-in-production
DEBUG=True
EURON_API_KEY=your-euron-api-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## Production Notes

⚠️ **This configuration is NOT suitable for production use**

For production deployment, you would need to:
- Set DEBUG=False
- Use a production database (PostgreSQL, MySQL)
- Configure proper ALLOWED_HOSTS
- Add security middleware and settings
- Use a proper web server (nginx + gunicorn)
- Set up static file serving
- Configure email backend
- Add logging and monitoring