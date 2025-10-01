# Django GenAI Application - Development Environment

A Django-based generative AI application with user authentication and conversation management using **Euron API**. This is configured specifically for **development environment only**.

## Features

- User authentication and registration
- AI-powered chat interface with **Euron AI API**
- Conversation history management
- Responsive web design
- Euron GPT-4.1-nano model integration
- SQLite database for development
- Debug mode enabled
- Development-optimized settings

## Development Setup

### Prerequisites

- Python 3.13.5 or compatible version
- pip package manager

### Installation Steps

1. **Create and activate virtual environment:**
```cmd
python -m venv venv
venv\Scripts\activate
```

2. **Install dependencies:**
```cmd
pip install -r requirements.txt
```

3. **Configure Euron API Key:**
   - Open the `.env` file in the root directory
   - Replace `your-euron-api-key-here` with your actual Euron API key
   - Get your API key from: https://api.euron.one

4. **Test Euron API setup:**
```cmd
python test_euron_api.py
```

5. **Run database migrations:**
```cmd
python manage.py migrate
```

6. **Create a superuser (optional):**
```cmd
python manage.py createsuperuser
```

7. **Start the development server:**
```cmd
python manage.py runserver
```

## Usage

1. Navigate to `http://127.0.0.1:8000/`
2. Register a new account or login
3. Start chatting with the AI assistant
4. View your conversation history
5. Access admin panel at `http://127.0.0.1:8000/admin/` (if superuser created)

## Development Configuration

- **Database:** SQLite (db.sqlite3)
- **Debug Mode:** Always enabled
- **Static Files:** Served by Django development server
- **Allowed Hosts:** localhost, 127.0.0.1, 0.0.0.0
- **Email Backend:** Console (for development testing)

## Project Structure

```
├── genai_project/          # Main Django project settings
├── chat/                   # AI chat functionality
├── accounts/               # User authentication
├── static/                 # Static files (CSS, JS, Images)
├── templates/              # HTML templates
├── db.sqlite3             # SQLite database
├── .env                   # Environment variables
└── manage.py              # Django management script
```

## Environment Variables (.env)

```env
SECRET_KEY=django-insecure-dev-key-only-for-development-change-in-production
DEBUG=True
EURON_API_KEY=your-euron-api-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## Development Notes

- This application is configured **only for development**
- All production-related configurations have been removed
- Database uses SQLite for simplicity
- No production security settings are enabled
- Static files are served by Django's development server

## Available VS Code Tasks

- "Install Dependencies" - Install Python packages
- "Django Migrate" - Run database migrations  
- "Create Superuser" - Create admin user
- "Django Development Server" - Start the development server
- "Django Setup All" - Run installation and migration in sequence