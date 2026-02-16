# Quick Start Guide - SecureGate RBAC

## Overview
This guide will help you get the SecureGate RBAC system running with all the new features:
- ✅ Authentication & JWT tokens
- ✅ Protected resources (GET /resource)
- ✅ Admin role assignment (POST /admin/assign-role)
- ✅ Authorization Middleware

## Prerequisites
- Python 3.8+
- PostgreSQL running locally
- pip packages installed

## Step 1: Setup Database

First, ensure PostgreSQL is running, then initialize the database:

```bash
python setup_db.py
```

**Output:**
```
✓ Database 'progres' created successfully
✓ Database tables created successfully
✓ Permissions created: READ_DATA, WRITE_DATA, ADMIN
✓ Roles created: Admin, User
✓ Test users created:
  - admin user (password: admin123) with Admin role and all permissions
  - user user (password: user123) with User role and READ_DATA permission
```

## Step 2: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 3: Start the Server

```bash
python serve.py
```

Or if you prefer using uvicorn directly:

```bash
python -m uvicorn backend.app.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

## Step 4: Test the Endpoints

### Option A: Using cURL

#### 4.1 Login to get a token
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "admin"
}
```

Copy the token value for the next steps.

#### 4.2 Access Protected Resource
```bash
curl -X GET "http://localhost:8000/resource" \
  -H "Authorization: Bearer <YOUR_TOKEN_HERE>" \
  -H "Content-Type: application/json"
```

**Response:**
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

#### 4.3 Assign a Role (Admin Only)
```bash
curl -X POST "http://localhost:8000/admin/assign-role" \
  -H "Authorization: Bearer <YOUR_TOKEN_HERE>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2, "role_id": 1}'
```

**Response:**
```json
{
  "status": "Role assigned"
}
```

### Option B: Using Python Test Script

We provide a comprehensive test script:

```bash
python test_api.py
```

This will run all tests automatically and show you the results.

### Option C: Using Swagger UI

Open your browser and go to:
```
http://localhost:8000/docs
```

You can test all endpoints interactively from there!

## Understanding the Permission System

### Default Users
| Username | Password | Role | Permissions |
|----------|----------|------|-------------|
| admin | admin123 | Admin | READ_DATA, WRITE_DATA, ADMIN |
| user | user123 | User | READ_DATA |

### Available Permissions
- `READ_DATA` - Can access /resource endpoint
- `WRITE_DATA` - Can write data (available for future use)
- `ADMIN` - Can assign roles, manage users

### Permission Requirements by Endpoint
| Endpoint | Method | Required Permission |
|----------|--------|-------------------|
| /auth/login | POST | - (Public) |
| /resource | GET | READ_DATA |
| /admin/assign-role | POST | ADMIN |

## Testing Scenarios

### Scenario 1: Admin Access Everything
```bash
# 1. Login as admin
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | jq -r '.token')

# 2. Access protected resource
curl -X GET "http://localhost:8000/resource" \
  -H "Authorization: Bearer $TOKEN"

# 3. Assign role
curl -X POST "http://localhost:8000/admin/assign-role" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2, "role_id": 1}'
```

### Scenario 2: Regular User Limited Access
```bash
# 1. Login as regular user
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "user123"}' | jq -r '.token')

# 2. Access protected resource (SUCCESS - has READ_DATA)
curl -X GET "http://localhost:8000/resource" \
  -H "Authorization: Bearer $TOKEN"

# 3. Assign role (FAIL - no ADMIN permission)
curl -X POST "http://localhost:8000/admin/assign-role" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2, "role_id": 1}'
# Returns: {"detail": "Permission 'ADMIN' required"}
```

### Scenario 3: No Token
```bash
# Try to access resource without token
curl -X GET "http://localhost:8000/resource"
# Returns: {"detail": "Missing authorization header"}
```

## Architecture Overview

### Authentication Flow
```
User Credentials
    ↓
POST /auth/login
    ↓
JWT Token Created (valid for 1 hour)
    ↓
Token returned to client
    ↓
Client includes in "Authorization: Bearer <token>" header
```

### Authorization Flow
```
Request to Protected Route
    ↓
AuthorizationMiddleware validates token
    ↓
Token decoded, user_id extracted
    ↓
Route handler checks specific permission
    ↓
if user has permission → execute route
if not → return 403 Forbidden
```

### Database Schema
```
Users (1) ←→ (M) User_Roles ←→ (M) Roles
                                      ↓
                            (M) Role_Permissions ← (M) Permissions
```

## Troubleshooting

### Issue: "Database connection error"
**Solution:** Make sure PostgreSQL is running and the credentials in setup_db.py match your configuration.

### Issue: "Invalid token"
**Solution:** 
1. Make sure you're using the token from the login response
2. Check token hasn't expired (tokens expire after 1 hour)
3. Use the exact token - no extra spaces

### Issue: "Permission denied"
**Solution:** 
1. Verify the user has the required role
2. Check the role has the required permission
3. Use `admin` user for testing /admin endpoints

### Issue: "User not found"
**Solution:** 
1. Verify the user_id exists in the database
2. Run setup_db.py to create test users

## Next Steps

### Further Enhancement Ideas
1. **Password Hashing** - Use bcrypt instead of plaintext passwords
2. **Registration** - Add POST /auth/register endpoint
3. **Refresh Tokens** - Implement token refresh mechanism
4. **Audit Logging** - Log all authorization attempts
5. **Rate Limiting** - Prevent brute force attacks
6. **Frontend Integration** - Connect with your dashboard

### Files to Review
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Full API reference
- [backend/app/main.py](backend/app/main.py) - FastAPI application setup
- [backend/app/middleware.py](backend/app/middleware.py) - Authorization middleware
- [backend/app/models.py](backend/app/models.py) - Database models
- [backend/app/routes/](backend/app/routes/) - All endpoint implementations

## Support

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

For questions or issues, check the project's TODO.md for current status.
