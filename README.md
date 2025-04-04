# Healthcare Backend System

A Django-based backend system for managing healthcare services, including patient-doctor relationships, authentication, and medical data management.

## Project Overview

This healthcare backend system provides a robust API for managing:
- User authentication and authorization
- Doctor profiles and specializations
- Patient records and medical history
- Patient-Doctor mapping and appointments

## Project Structure

```
healthcare/          # Main project directory
├── authentication/   # User authentication module
├── doctors/         # Doctor management module
├── patients/        # Patient management module
├── healthcare/      # Project settings and main URLs
└── manage.py        # Django management script
```

## Setup and Installation

1. Clone the repository

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register/`: Register a new user
- `POST /api/auth/login/`: Login and get authentication token

### Doctors
- `GET /api/doctors/`: List all doctors
- `POST /api/doctors/`: Create a new doctor profile
- `GET /api/doctors/<id>/`: Get doctor details
- `PUT /api/doctors/<id>/`: Update doctor information

### Patients
- `GET /api/patients/`: List all patients
- `POST /api/patients/`: Create a new patient record
- `GET /api/patients/<id>/`: Get patient details
- `PUT /api/patients/<id>/`: Update patient information

### Patient-Doctor Mapping
- `POST /api/patients/mapping/`: Assign doctor to patient
- `GET /api/patients/mapping/<id>/`: Get patient's assigned doctors

## Authentication

The system uses token-based authentication. Include the token in the Authorization header:
```
Authorization: Token <your-token-here>
```

## Development

- Run tests: `python manage.py test`
- Check API endpoints: `python test_api.py`

## Security

- Implements token-based authentication
- Secure password hashing
- Role-based access control
- Input validation and sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.