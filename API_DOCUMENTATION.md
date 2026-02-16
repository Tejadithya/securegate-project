# SecureGate RBAC API Documentation

## Overview
This document describes the latest additions to the SecureGate RBAC System API, including the protected resource endpoint, assignment of roles, and the authorization middleware.

## Implemented Features

### 1. **GET /resource** - Protected Resource Endpoint
A protected route that only users with the `READ_DATA` permission can access.

**Endpoint:** `GET /resource`

**Authentication:** Required (Bearer Token)

**Required Permission:** `READ_DATA`

**Request Headers:**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "message": "You have access to this resource",
  "user_id": 1,
  "username": "admin",
  "data": {
    "content": "This is protected resource data",
    "timestamp": "2026-02-15T00:00:00Z"
  }
}
```

**Error Responses:**
- **401 Unauthorized** - Missing or invalid token
```json
{
  "detail": "Invalid token"
}
```

- **403 Forbidden** - User lacks READ_DATA permission
```json
{
  "detail": "Permission 'READ_DATA' required"
}
```

**Example Usage:**
```bash
curl -X GET "http://localhost:8000/resource" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json"
```

---

### 2. **POST /admin/assign-role** - Assign Role to User
An admin-only route to change or assign a user's role. Only users with the `ADMIN` permission can access this endpoint.

**Endpoint:** `POST /admin/assign-role`

**Authentication:** Required (Bearer Token)

**Required Permission:** `ADMIN`

**Request Headers:**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": 2,
  "role_id": 1
}
```

**Response (200 OK):**
```json
{
  "status": "Role assigned"
}
```

**Error Responses:**
- **401 Unauthorized** - Missing or invalid token
```json
{
  "detail": "Invalid token"
}
```

- **403 Forbidden** - User lacks ADMIN permission
```json
{
  "detail": "Permission 'ADMIN' required"
}
```

- **404 Not Found** - User or role not found
```json
{
  "detail": "User not found"
}
```

**Example Usage:**
```bash
curl -X POST "http://localhost:8000/admin/assign-role" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "role_id": 1
  }'
```

---

### 3. **Authorization Middleware**
A custom middleware that validates JWT tokens for protected routes and checks authorization.

**How It Works:**
- Automatically validates JWT tokens in the `Authorization` header
- Enforces authentication on routes starting with `/resource` and `/admin`
- Returns descriptive error messages for authentication failures

**Protected Routes:**
- `/resource/*`
- `/admin/*`

**Token Format:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Middleware Features:**
- ✅ Validates JWT signature
- ✅ Checks token expiration
- ✅ Validates against SECRET_KEY
- ✅ Routes user_id to request state for downstream handlers
- ✅ Returns 401 for invalid/missing tokens
- ✅ Returns descriptive error messages

---

## Database Setup

### Required Tables
The system uses the following database tables:

1. **users** - User accounts
   - id (PK)
   - username (UNIQUE)
   - password

2. **roles** - User roles
   - id (PK)
   - name (UNIQUE)

3. **permissions** - Permissions
   - id (PK)
   - name (UNIQUE)

4. **user_roles** - User-Role mappings (Many-to-Many)
   - user_id (FK)
   - role_id (FK)

5. **role_permissions** - Role-Permission mappings (Many-to-Many)
   - role_id (FK)
   - permission_id (FK)

### Initialization

Run the setup script to initialize the database:

```bash
python setup_db.py
```

This will:
1. Create the `progres` database
2. Create all required tables
3. Insert default permissions: `READ_DATA`, `WRITE_DATA`, `ADMIN`
4. Insert default roles: `Admin`, `User`
5. Create test users:
   - **admin** (password: admin123) - Has Admin role with all permissions
   - **user** (password: user123) - Has User role with READ_DATA permission

---

## Authentication Flow

### 1. Login
First, login to get a JWT token:

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "admin"
}
```

### 2. Use Token for Protected Endpoints
Include the token in the `Authorization` header:

```bash
curl -X GET "http://localhost:8000/resource" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 3. Token Details
- **Expiration:** 1 hour from creation
- **Algorithm:** HS256
- **Secret Key:** `supersecret`
- **Claims:** `sub` (user_id), `exp` (expiration timestamp)

---

## Permission Matrix

| Role | Permissions | Endpoints |
|------|-------------|-----------|
| **Admin** | READ_DATA, WRITE_DATA, ADMIN | `/resource`, `/admin/assign-role` |
| **User** | READ_DATA | `/resource` |

---

## Error Handling

### Common Error Responses

**401 Unauthorized:**
- Missing Authorization header
- Invalid or expired token
- Malformed JWT

**403 Forbidden:**
- User authenticated but lacks required permission
- User is not assigned any role with required permission

**404 Not Found:**
- User or role doesn't exist in the database

---

## Example Workflow

### Step 1: Setup Database
```bash
python setup_db.py
```

### Step 2: Start Server
```bash
python -m uvicorn backend.app.main:app --reload
```

### Step 3: Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Response: {"token": "...", "username": "admin"}
```

### Step 4: Access Protected Resource
```bash
curl -X GET "http://localhost:8000/resource" \
  -H "Authorization: Bearer <TOKEN>"
```

### Step 5: Assign Role (Admin Only)
```bash
curl -X POST "http://localhost:8000/admin/assign-role" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2, "role_id": 1}'
```

---

## Configuration

### Environment Variables
- `SECRET_KEY`: JWT signing key (default: "supersecret")
- `ALGORITHM`: JWT algorithm (default: "HS256")
- `DATABASE_URL`: PostgreSQL connection string

### Frontend CORS Setup
The API allows requests from:
- `http://localhost:3000` (React dev server)
- `http://localhost:8000` (Swagger UI)
- `file://` (Local file access)

---

## Testing

### Using Swagger UI
Navigate to: `http://localhost:8000/docs`

All endpoints are documented and can be tested directly from the Swagger UI.

### Using Thunder Client / Postman
Import the API documentation or use the curl examples provided above.
