# User Management API

This is a Django-based User Management API that handles user registration, user detail management, and search functionalities. The API ensures robust validation to prevent duplicate entries and enforces security best practices.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git https://github.com/kashyaap/UserApp.git
cd UserApp
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For MacOS/Linux
venv\Scripts\activate    # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

---

## API Endpoints

### 1. User Registration (Sign Up)

**Endpoint:**

```
POST /api/signup/
```

**Request Body (JSON):**

```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "phone_number": "1234567890",
  "password": "securepassword",
  "bio": "Loves coding"
}
```

**Response (Success):**

```json
{
  "message": "User registered successfully."
}
```

**Response (Validation Error - Duplicate Username):**

```json
{
  "error": {
    "username": "This username is already taken."
  }
}
```

**Response (Duplicate Phone and Email):**

```json
{
  "error": {
    "error": "User with this phone number and email already exists."
  }
}
```

---

### 2. Search Users by Phone or Email

**Endpoint:**

```
POST /api/search/
```

**Request Body (JSON):**

```json
{
  "phone_number": "1234567890"
}
```

**Response (Success):**

```json
[
  {
    "username": "johndoe",
    "email": "johndoe@example.com",
    "phone_number": "1234567890",
    "bio": "Loves coding"
  }
]
```

**Response (No Match):**

```json
{
  "message": "No users found with matching details."
}
```

---

## Contact

**Author:** Abhinav Kashyap
