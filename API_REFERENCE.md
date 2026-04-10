# Smart Locker System - API Reference

Complete JSON input/output examples for all API endpoints.

**Base URL:** `http://127.0.0.1:8000/api`

**Authentication:** JWT Bearer Token (except login/register endpoints)

---

## Table of Contents
1. [Authentication Endpoints](#authentication-endpoints)
2. [Locker Endpoints](#locker-endpoints)
3. [Reservation Endpoints](#reservation-endpoints)
4. [API Root](#api-root)

---

## Authentication Endpoints

### 1. Register User

**Endpoint:** `POST /api/auth/register/`

**Access:** Public (No authentication required)

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john.doe@example.com",
  "name": "John Doe",
  "password": "SecurePass123!"
}
```

**Success Response (201 Created):**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@example.com",
    "name": "John Doe",
    "role": "user",
    "is_active": true
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "username": ["A user with that username already exists."],
  "email": ["Enter a valid email address."]
}
```

---

### 2. Login

**Endpoint:** `POST /api/auth/login/`

**Access:** Public (No authentication required)

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@example.com",
    "name": "John Doe",
    "role": "user",
    "is_active": true
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "No active account found with the given credentials"
}
```

---

### 3. Token Refresh

**Endpoint:** `POST /api/auth/token/refresh/`

**Access:** Public (No authentication required)

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

---

### 4. Get User Profile

**Endpoint:** `GET /api/auth/profile/`

**Access:** Authenticated users only

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john.doe@example.com",
  "name": "John Doe",
  "role": "user",
  "is_active": true
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Locker Endpoints

### 5. List All Lockers

**Endpoint:** `GET /api/lockers/`

**Access:** Authenticated users only

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Query Parameters (Optional):**
- `page` - Page number (default: 1)
- `status` - Filter by status (available, occupied, maintenance, deactivated)
- `size` - Filter by size (small, medium, large)
- `location` - Filter by location

**Example:** `GET /api/lockers/?status=available&size=medium`

**Success Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/lockers/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "locker_number": "A001",
      "location": "Building A - Floor 1",
      "size": "medium",
      "status": "available",
      "created_at": "2026-04-10T10:30:00Z",
      "updated_at": "2026-04-10T10:30:00Z"
    },
    {
      "id": 2,
      "locker_number": "A002",
      "location": "Building A - Floor 1",
      "size": "large",
      "status": "occupied",
      "created_at": "2026-04-10T10:35:00Z",
      "updated_at": "2026-04-10T11:00:00Z"
    }
  ]
}
```

---

### 6. Get Locker Details

**Endpoint:** `GET /api/lockers/{id}/`

**Access:** Authenticated users only

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "locker_number": "A001",
  "location": "Building A - Floor 1",
  "size": "medium",
  "status": "available",
  "created_at": "2026-04-10T10:30:00Z",
  "updated_at": "2026-04-10T10:30:00Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

### 7. Create Locker (Admin Only)

**Endpoint:** `POST /api/lockers/`

**Access:** Admin users only

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Request Body:**
```json
{
  "locker_number": "B105",
  "location": "Building B - Floor 1",
  "size": "large",
  "status": "available"
}
```

**Field Descriptions:**
- `locker_number` (string, required): Unique identifier for the locker
- `location` (string, required): Physical location description
- `size` (string, required): One of: `small`, `medium`, `large`
- `status` (string, optional): One of: `available`, `occupied`, `maintenance`, `deactivated` (default: `available`)

**Success Response (201 Created):**
```json
{
  "id": 26,
  "locker_number": "B105",
  "location": "Building B - Floor 1",
  "size": "large",
  "status": "available",
  "created_at": "2026-04-10T12:00:00Z",
  "updated_at": "2026-04-10T12:00:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "locker_number": ["locker with this locker number already exists."]
}
```

**Error Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 8. Update Locker (Admin Only)

**Endpoint:** `PUT /api/lockers/{id}/`

**Access:** Admin users only

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Request Body:**
```json
{
  "locker_number": "B105",
  "location": "Building B - Floor 2",
  "size": "medium",
  "status": "maintenance"
}
```

**Success Response (200 OK):**
```json
{
  "id": 26,
  "locker_number": "B105",
  "location": "Building B - Floor 2",
  "size": "medium",
  "status": "maintenance",
  "created_at": "2026-04-10T12:00:00Z",
  "updated_at": "2026-04-10T12:15:00Z"
}
```

---

### 9. Partial Update Locker (Admin Only)

**Endpoint:** `PATCH /api/lockers/{id}/`

**Access:** Admin users only

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Request Body (Partial - only include fields to update):**
```json
{
  "status": "available"
}
```

**Success Response (200 OK):**
```json
{
  "id": 26,
  "locker_number": "B105",
  "location": "Building B - Floor 2",
  "size": "medium",
  "status": "available",
  "created_at": "2026-04-10T12:00:00Z",
  "updated_at": "2026-04-10T12:20:00Z"
}
```

---

### 10. Delete/Deactivate Locker (Admin Only)

**Endpoint:** `DELETE /api/lockers/{id}/`

**Access:** Admin users only

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Success Response (204 No Content):**
- No response body

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

### 11. Get Available Lockers

**Endpoint:** `GET /api/lockers/available/`

**Access:** Authenticated users only

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Success Response (200 OK):**
```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "locker_number": "A001",
      "location": "Building A - Floor 1",
      "size": "medium",
      "status": "available",
      "created_at": "2026-04-10T10:30:00Z",
      "updated_at": "2026-04-10T10:30:00Z"
    },
    {
      "id": 5,
      "locker_number": "A005",
      "location": "Building A - Floor 2",
      "size": "small",
      "status": "available",
      "created_at": "2026-04-10T10:45:00Z",
      "updated_at": "2026-04-10T10:45:00Z"
    }
  ]
}
```

---

## Reservation Endpoints

### 12. List User Reservations

**Endpoint:** `GET /api/reservations/`

**Access:** Authenticated users only

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Query Parameters (Optional):**
- `page` - Page number (default: 1)
- `status` - Filter by status (active, released, expired)

**Example:** `GET /api/reservations/?status=active`

**Success Response (200 OK):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "locker": 1,
      "locker_number": "A001",
      "locker_location": "Building A - Floor 1",
      "user": 1,
      "status": "active",
      "reserved_at": "2026-04-10T11:00:00Z",
      "released_at": null,
      "created_at": "2026-04-10T11:00:00Z",
      "updated_at": "2026-04-10T11:00:00Z"
    },
    {
      "id": 2,
      "locker": 3,
      "locker_number": "A003",
      "locker_location": "Building A - Floor 1",
      "user": 1,
      "status": "released",
      "reserved_at": "2026-04-09T09:00:00Z",
      "released_at": "2026-04-09T17:00:00Z",
      "created_at": "2026-04-09T09:00:00Z",
      "updated_at": "2026-04-09T17:00:00Z"
    }
  ]
}
```

---

### 13. Get Reservation Details

**Endpoint:** `GET /api/reservations/{id}/`

**Access:** Authenticated users only (owner or admin)

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "locker": 1,
  "locker_number": "A001",
  "locker_location": "Building A - Floor 1",
  "user": 1,
  "status": "active",
  "reserved_at": "2026-04-10T11:00:00Z",
  "released_at": null,
  "created_at": "2026-04-10T11:00:00Z",
  "updated_at": "2026-04-10T11:00:00Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

### 14. Create Reservation

**Endpoint:** `POST /api/reservations/`

**Access:** Authenticated users only

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Request Body:**
```json
{
  "locker_id": 1
}
```

**Field Descriptions:**
- `locker_id` (integer, required): ID of the locker to reserve

**Success Response (201 Created):**
```json
{
  "id": 3,
  "locker": 1,
  "locker_number": "A001",
  "locker_location": "Building A - Floor 1",
  "user": 1,
  "status": "active",
  "reserved_at": "2026-04-10T12:30:00Z",
  "released_at": null,
  "created_at": "2026-04-10T12:30:00Z",
  "updated_at": "2026-04-10T12:30:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Locker is not available"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "You already have an active reservation"
}
```

---

### 15. Release Locker

**Endpoint:** `PUT /api/reservations/{id}/release/`

**Access:** Authenticated users only (owner or admin)

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Request Body:** None required

**Success Response (200 OK):**
```json
{
  "id": 1,
  "locker": 1,
  "locker_number": "A001",
  "locker_location": "Building A - Floor 1",
  "user": 1,
  "status": "released",
  "reserved_at": "2026-04-10T11:00:00Z",
  "released_at": "2026-04-10T15:30:00Z",
  "created_at": "2026-04-10T11:00:00Z",
  "updated_at": "2026-04-10T15:30:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Reservation is already released"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

### 16. Delete Reservation (Admin Only)

**Endpoint:** `DELETE /api/reservations/{id}/`

**Access:** Admin users only

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Success Response (204 No Content):**
- No response body

**Error Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## API Root

### 17. API Documentation

**Endpoint:** `GET /`

**Access:** Public (No authentication required)

**Success Response (200 OK):**
```json
{
  "message": "Smart Locker System REST API",
  "endpoints": {
    "auth": {
      "register": "/api/auth/register/",
      "login": "/api/auth/login/",
      "token_refresh": "/api/auth/token/refresh/",
      "profile": "/api/auth/profile/"
    },
    "lockers": {
      "list_create": "/api/lockers/",
      "detail": "/api/lockers/{id}/",
      "available": "/api/lockers/available/"
    },
    "reservations": {
      "list_create": "/api/reservations/",
      "detail": "/api/reservations/{id}/",
      "release": "/api/reservations/{id}/release/"
    },
    "admin": "/admin/"
  },
  "documentation": "All endpoints require authentication except register, login, and token_refresh"
}
```

---

## Common HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Request successful, no content returned |
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Authentication required or invalid credentials |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error - Server error |

---

## Authentication Examples

### Using curl

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "SecurePass123!"}'
```

**Get Profile (with token):**
```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Create Locker (Admin):**
```bash
curl -X POST http://127.0.0.1:8000/api/lockers/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -d '{"locker_number": "B105", "location": "Building B - Floor 1", "size": "large"}'
```

### Using Python requests

```python
import requests

API_BASE = "http://127.0.0.1:8000/api"

# Login
login_response = requests.post(f"{API_BASE}/auth/login/", json={
    "username": "johndoe",
    "password": "SecurePass123!"
})
token = login_response.json()["access"]

# Set headers for authenticated requests
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Get available lockers
lockers = requests.get(f"{API_BASE}/lockers/available/", headers=headers)
print(lockers.json())

# Create reservation
reservation = requests.post(f"{API_BASE}/reservations/", json={
    "locker_id": 1
}, headers=headers)
print(reservation.json())
```

### Using JavaScript (Fetch API)

```javascript
const API_BASE = 'http://127.0.0.1:8000/api';

// Login
const loginResponse = await fetch(`${API_BASE}/auth/login/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'johndoe',
    password: 'SecurePass123!'
  })
});

const { access: token } = await loginResponse.json();

// Get profile
const profileResponse = await fetch(`${API_BASE}/auth/profile/`, {
  headers: { 'Authorization': `Bearer ${token}` }
});

const profile = await profileResponse.json();
console.log(profile);

// Create reservation
const reservationResponse = await fetch(`${API_BASE}/reservations/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({ locker_id: 1 })
});

const reservation = await reservationResponse.json();
console.log(reservation);
```

---

## Notes

1. **Token Expiry:** Access tokens expire after 60 minutes. Use the refresh token to get a new access token.
2. **Pagination:** List endpoints return paginated results (20 items per page by default).
3. **Date Format:** All dates are in ISO 8601 format (UTC timezone).
4. **Admin Access:** Admin endpoints require users with `role: "admin"`.
5. **Locker Status Values:** `available`, `occupied`, `maintenance`, `deactivated`
6. **Locker Size Values:** `small`, `medium`, `large`
7. **Reservation Status Values:** `active`, `released`, `expired`
