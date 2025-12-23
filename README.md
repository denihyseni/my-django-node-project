# Project README

## University Portal - Secure Student Management System

A comprehensive web application for managing students, professors, courses, and enrollments with advanced security features.

### Features

✨ **Core Features**
- Student & Professor Management
- Course Management & Scheduling
- Enrollment System
- Grade Management
- Role-based Access Control (Admin, Professor, Student)

🔒 **Security Features**
- JWT Token Authentication with HttpOnly Cookies
- Token Blacklisting & Rotation
- CSRF & XSS Protection
- Rate Limiting on Login Attempts
- Session Management with Auto-Expiry
- Security Event Logging
- Encrypted Password Storage (bcrypt)

📊 **Admin Dashboard**
- Full system overview with statistics
- Create and manage professors and students
- Assign courses to professors
- Edit user details and passwords
- Subject management

👨‍🏫 **Professor Dashboard**
- View assigned courses
- Manage student enrollments
- Grade students
- Track student progress

👨‍🎓 **Student Dashboard**
- View enrolled courses
- Track grades
- Monitor academic progress
- Course details and descriptions

---

## Tech Stack

**Backend**
- Django 5.2.9
- Django REST Framework 3.14.0
- Python 3.11+
- SQLite (development) / PostgreSQL (production)

**Frontend**
- React 18+
- React Router
- Axios
- CSS3

**Security**
- djangorestframework-simplejwt
- PyJWT
- django-cors-headers

---

## Project Structure

```
Assignment1/
├── project/
│   ├── settings.py          # Django configuration
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
│
├── university/
│   ├── models.py            # Database models
│   ├── views.py             # API views
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URLs
│   ├── secure_auth_views.py # Authentication endpoints
│   ├── security_models.py   # Security tracking models
│   └── migrations/          # Database migrations
│
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main app component
│   │   ├── Login.js         # Login component
│   │   ├── LoginSecure.js   # Secure login (HttpOnly)
│   │   ├── pages/
│   │   │   ├── AdminDashboard.js
│   │   │   ├── ProfessorDashboard.js
│   │   │   └── StudentDashboard.js
│   │   ├── styles.css       # Global styles
│   │   └── index.js         # React entry point
│   ├── public/
│   │   └── index.html
│   └── package.json
│
├── scripts/
│   ├── test_crud.py         # CRUD testing
│   ├── test_dashboards.py   # Dashboard testing
│   ├── test_permissions.py  # Permission testing
│   └── api_test.py          # API testing
│
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
├── DEPLOYMENT_GUIDE.md     # Deployment instructions
└── README.md               # This file
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+
- Git

### Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd Assignment1
   ```

2. **Setup Backend**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   cd project
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

### Test Credentials

| Role | Username | Password | Notes |
|------|----------|----------|-------|
| Admin | admin_user | admin123 | Full system access |
| Professor | professor1 | prof123 | Can manage courses & grades |
| Student | student1 | student123 | Can view enrollments & grades |

---

## Authentication Flow

### Login
1. User enters credentials on `/login`
2. Backend validates and returns JWT tokens
3. Access token stored in localStorage (for Authorization header)
4. Refresh token stored as HttpOnly cookie
5. User redirected to dashboard based on role

### Token Expiry & Refresh
- Access tokens expire after **15 minutes**
- Refresh tokens expire after **7 days**
- Tokens automatically rotate on refresh
- Old tokens are blacklisted

### Logout
1. User clicks Logout button
2. All tokens are blacklisted on backend
3. All sessions are deleted
4. Cookies are cleared
5. LocalStorage is cleared
6. User redirected to login

---

## API Endpoints

### Authentication
- `POST /api/auth/token/` - Login
- `POST /api/auth/token/refresh/` - Refresh token
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/sessions/` - List user sessions
- `POST /api/auth/sessions/{id}/revoke/` - Revoke session

### University Management
- `GET/POST /api/university/faculties/` - Faculties
- `GET/POST /api/university/professors/` - Professors
- `GET/POST /api/university/students/` - Students
- `GET/POST /api/university/subjects/` - Subjects
- `GET/POST /api/university/enrollments/` - Enrollments
- `GET /api/university/dashboard/` - Dashboard stats

---

## Database Models

### User-Related
- **User** - Django built-in user model
- **Administrator** - Admin profile
- **Professor** - Professor profile with title
- **Student** - Student profile with enrollment number

### Academic
- **Faculty** - Computer Science, English, etc.
- **Subject** - Courses offered
- **Enrollment** - Student course enrollment with grades

### Security
- **TokenBlacklist** - Revoked tokens
- **UserSession** - Active user sessions
- **LoginAttempt** - Login attempt tracking
- **SecurityEvent** - Security audit log

---

## Security Features in Detail

### Token Storage
- **Access Token**: Stored in localStorage for Authorization headers
- **Refresh Token**: HttpOnly cookie (JavaScript cannot access)
- **Benefit**: Defense-in-depth against XSS attacks

### Session Management
- 15-minute inactivity timeout
- Session cleared on browser close
- Expired sessions cannot be accessed
- All active sessions tracked and revokable

### Rate Limiting
- Login attempts rate-limited per IP
- Prevents brute force attacks
- Logs failed attempts for security audit

### CSRF Protection
- SameSite=Strict cookies
- CSRF token validation
- Prevents cross-site request forgery

---

## Environment Variables

Create `.env` file in project root:

```
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Hosts
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# JWT
JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME=7
```

---

## Deployment

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

### Quick Deploy with Gunicorn
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn project.wsgi:application --bind 0.0.0.0:8000
```

---

## Testing

### Run API Tests
```bash
cd scripts
python api_test.py
python test_crud.py
python test_dashboards.py
python test_permissions.py
```

---

## Troubleshooting

**CORS Errors**: Update `CORS_ALLOWED_ORIGINS` in settings.py

**Token Issues**: Clear browser cookies and localStorage, log in again

**Database Errors**: Run `python manage.py migrate`

**Static Files Missing**: Run `python manage.py collectstatic`

---

## Git Push Checklist

- [ ] Created `.gitignore` with confidential files excluded
- [ ] Created `requirements.txt` with all dependencies
- [ ] Removed `db.sqlite3` from tracking
- [ ] Removed `.env` file from tracking
- [ ] Removed `venv/` directory from tracking
- [ ] Removed `node_modules/` from tracking
- [ ] Added `DEPLOYMENT_GUIDE.md` and `README.md`

**Push commands:**
```bash
git init
git add .
git commit -m "Initial commit: University Portal with JWT authentication"
git remote add origin <your-repo-url>
git push -u origin main
```

---

## Support & Resources

- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/
- **JWT**: https://jwt.io/
- **React**: https://react.dev/
- **Security**: https://owasp.org/

---

## License

This project is provided as-is for educational purposes.

---

## Contributors

- Development Team

---

**Last Updated**: December 23, 2025  
**Version**: 1.0.0
