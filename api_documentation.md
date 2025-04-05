# Healthcare API Documentation

## Authentication

### 1. User Registration

#### Patient Registration (POST /api/auth/register/)
```json
{
    "username": "testpatient",
    "password": "securepass123",
    "confirm_password": "securepass123",
    "email": "patient@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "address": "123 Test St",
    "date_of_birth": "1990-01-01",
    "user_type": "PATIENT"
}
```

#### Doctor Initial Registration (POST /api/auth/register/)
```json
{
    "username": "dr.smith",
    "password": "securepass123",
    "confirm_password": "securepass123",
    "email": "dr.smith@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "phone_number": "+1234567890",
    "address": "123 Medical Center Dr, City, State 12345",
    "date_of_birth": "1980-01-01",
    "user_type": "DOCTOR"
}
```

### 2. User Login (POST /api/auth/login/)
```json
{
    "username": "username",
    "password": "password"
}
```

### 3. User Logout (POST /api/auth/logout/)
Requires authentication token in request header and refresh token in request body.

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "refresh": "your_refresh_token"
}
```

**Response:**
- Success (205 Reset Content): Token successfully blacklisted
- Error (400 Bad Request): Invalid refresh token

### 4. Token Refresh (POST /api/auth/token/refresh/)
```json
{
    "refresh": "your_refresh_token"
}
```

## Patient Endpoints

### 1. Create/Update Patient Profile (POST/PUT /api/patients/)
Note: Requires authentication token
```json
{
    "user": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "patient@example.com",
        "phone_number": "+1234567890",
        "address": "123 Test St",
        "date_of_birth": "1990-01-01"
    },
    "blood_group": "A+",
    "allergies": "None",
    "medical_conditions": "None",
    "emergency_contact_name": "Emergency Contact",
    "emergency_contact_number": "9876543210"
}
```

### 2. Create Appointment (POST /api/appointments/)
Note: Requires authentication token
```json
{
    "doctor": 1,
    "appointment_date": "2024-01-20",
    "appointment_time": "10:00:00",
    "reason": "Regular checkup",
    "notes": "First visit",
    "status": "SCHEDULED"
}
```

### 3. Medical Records (POST /api/medical-records/)
Note: Requires authentication token
```json
{
    "patient": 1,
    "doctor": 1,
    "diagnosis": "Common cold",
    "prescription": "Rest and fluids",
    "notes": "Follow up in 1 week if symptoms persist"
}
```

## Doctor Endpoints

### 1. Create/Update Doctor Profile (POST/PUT /api/doctors/)
Note: Requires authentication token
```json
{
    "user": {
        "first_name": "John",
        "last_name": "Smith",
        "email": "dr.smith@example.com",
        "phone_number": "+1234567890",
        "address": "123 Medical Center Dr",
        "date_of_birth": "1980-01-01"
    },
    "specialization_id": 1,
    "license_number": "MED123456",
    "experience_years": 10,
    "consultation_fee": 150.00,
    "available_days": "Monday, Wednesday, Friday",
    "available_time_start": "09:00:00",
    "available_time_end": "17:00:00"
}
```

### 2. List Specializations (GET /api/specializations/)
Note: Requires authentication token

Response:
```json
[
    {
        "id": 1,
        "name": "Cardiology",
        "description": "Heart and cardiovascular system specialist"
    }
]
```

## Important Notes

1. Authentication:
   - All endpoints except registration and login require authentication
   - Add the token to request headers:
     ```
     Authorization: Bearer <your_token>
     ```

2. Data Formats:
   - Date format: YYYY-MM-DD
   - Time format: HH:MM:SS (24-hour format)
   - Available days should be comma-separated full day names
   - All IDs are integers
   - Monetary values (consultation_fee) are decimal numbers
   - The `specialization_id` should be a valid ID from the specializations table

3. Security:
   - Passwords should be strong and meet minimum security requirements
   - All sensitive data is transmitted over HTTPS
   - Tokens expire after a set period and must be renewed