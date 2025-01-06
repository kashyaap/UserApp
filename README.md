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

Ensure that **Pillow** is installed for handling image uploads:

```bash
pip install Pillow
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
  "bio": "Loves coding",
  "profile_picture": null
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

## Project Structure

```
UserApp/
│
├── UserApp/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│
├── api/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│
├── migrations/
│   ├── 0001_initial.py
│   ├── __init__.py
│
├── manage.py
└── requirements.txt
```

---

## Key Points of Implementation

### Models

- **UserDetail** – Extends Django’s User model by adding phone number, bio, and profile picture.
- **Unique Constraints** – Enforced on `username` and the combination of `phone_number` and `email` to prevent duplicates.

```python
class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
```

---

### Signals

- Automatically creates or updates `UserDetail` when a `User` is created/updated.

```python
@receiver(post_save, sender=User)
def create_or_update_user_detail(sender, instance, created, **kwargs):
    UserDetail.objects.update_or_create(user=instance)
```

---

### Error Handling

- **ValidationError** – Raised for duplicate usernames or phone/email combinations.
- **IntegrityError** – Caught and handled to avoid server crashes when a unique constraint fails.

```python
except IntegrityError:
    return Response(
        {"error": "A user with these details already exists."},
        status=status.HTTP_400_BAD_REQUEST
    )
```

## Contact

**Author:** Abhinav Kashyap
