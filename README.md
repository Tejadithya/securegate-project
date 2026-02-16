# SecureGate RBAC System

## Day-by-Day Work Log (7 Days)

### Day 1: Project Initialization & Database Setup
- Created TODO.md to track project progress
- Set up PostgreSQL database configuration in backend/app/database.py
- Added python-dotenv to backend/requirements.txt for environment variable management
- Created .env file with PostgreSQL configuration
- Designed and set up database schema with tables for users, roles, and permissions

### Day 2: Authentication System Implementation
- Implemented login endpoint (POST /auth/login)
- Generated JWT tokens on successful authentication
- Added JWT validation and verification logic
- Created authentication service for handling user credentials

### Day 3: RBAC & Authorization Foundation
- Created User, Role, and Permission models
- Set up Many-to-Many relationships between models
- Implemented require_permission dependency for route protection
- Created permission checking logic in RBAC service

### Day 4: Protected Routes Development
- Implemented GET /resource endpoint with READ_DATA permission requirement
- Implemented POST /admin/assign-role endpoint with ADMIN permission requirement
- Added permission checks to all route handlers
- Created admin routes for role management

### Day 5: Authorization Middleware
- Created custom AuthorizationMiddleware for request validation
- Implemented JWT token validation for protected routes
- Added user permissions examination and validation logic
- Integrated descriptive error messages for authorization failures
- Connected middleware to FastAPI application

### Day 6: Database Initialization & Test Data
- Updated setup_db.py with roles and permissions seeding
- Created test users with appropriate roles
- Assigned permissions to roles
- Added default data seeding for initial setup

### Day 7: Documentation & API Reference
- Created comprehensive API documentation
- Documented all endpoints with examples
- Provided curl examples for testing
- Documented authentication flow
- Created troubleshooting guide

---
output:
# 1. Initialize database
python setup_db.py

# 2. Start server
python serve.py

# 3. Test all endpoints
python test_api.py

## Testing Coverage

The `test_api.py` script covers:
1. ✓ Admin login
2. ✓ User login
3. ✓ Admin /resource access
4. ✓ User /resource access
5. ✓ Unauthorized /resource access
6. ✓ Admin role assignment
7. ✓ User unauthorized role assignment attempt

---

terminal output:

PS C:\Users\Teja Dithya\Music\securegate project> python test_api.py
Starting SecureGate RBAC API Tests...
Make sure the server is running: python serve.py


============================================================
SECUREGATE RBAC - FULL TEST SUITE
============================================================

============================================================
Testing: POST /auth/login - admin
============================================================
✓ Admin token obtained

✓ PASSED: Login as admin
  Response: {
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZXhwIjoxNzcxMTQ2ODEyfQ.DzEpYpwT-ip4DRhqG_gEtstg1BqpB-6NoMbB6u2qQO4",
  "username": "admin"
}

============================================================
Testing: POST /auth/login - user
============================================================
✓ User token obtained

✓ PASSED: Login as user
  Response: {
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNzcxMTQ2ODEyfQ.cJ2CM69q4XISt56HZuLwrbbao1rqWx7mmA18OYF9Qeg",
  "username": "user"
}

============================================================
Testing: GET /resource - admin
============================================================

✓ PASSED: Access /resource as admin
  └─ Status 200
  Response: {
  "message": "You have access to this resource",
  "user_id": 5,
  "username": "admin",
  "data": {
    "content": "This is protected resource data",
    "timestamp": "2026-02-15T00:00:00Z"
  }
}

============================================================
Testing: GET /resource - user
============================================================

✓ PASSED: Access /resource as user
  └─ Status 200
  Response: {
  "message": "You have access to this resource",
  "user_id": 6,
  "username": "user",
  "data": {
    "content": "This is protected resource data",
    "timestamp": "2026-02-15T00:00:00Z"
  }
}

============================================================
Testing: GET /resource - Without Token (Should Fail)
============================================================

✓ PASSED: Unauthorized access without token
  └─ Expected 401/422, got 401
  Response: {
  "detail": "Missing authorization header"
}

============================================================
Testing: POST /admin/assign-role - Regular User (Should Fail)
============================================================

✓ PASSED: Unauthorized assign-role (regular user)
  └─ Expected 403, got 403
  Response: {
  "detail": "Permission 'ADMIN' required"
}

============================================================
Testing: POST /admin/assign-role - Admin Only
============================================================

✓ PASSED: Assign role to user 6
  └─ Status 200
  Response: {
  "status": "Role assigned"
}


============================================================
TEST SUMMARY
============================================================
✓ Login as admin
✓ Login as user
✓ Admin access /resource
✓ User access /resource
✓ Unauthorized resource access
✓ User unauthorized assign role
✓ Admin assign role

Total: 7/7 tests passed
============================================================

✓ ALL TESTS PASSED!

---

## Setup
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload


#graph TD
#Controller --> Service
#Service --> Repository
#Repository --> Database


SecureGate RBAC System
Setup

pip install -r requirements.txt
uvicorn app.main:app --reload


#graph TD
#Controller --> Service
#Service --> Repository
#Repository --> Database



Regarding testing: I have not performed any testing yet on the project.

Remaining areas that require coverage include:
- Running the FastAPI app to check if it starts without errors.
- Testing the login endpoint for authentication.
- Testing the assign-role endpoint for authorization.
- Running the existing test in test_authorization.py to see if it passes or fails.
- Checking database connectivity and table creation.
- Verifying JWT token handling and permission checks.





graph TD

subgraph Frontend
    View[HTML + Bootstrap UI]
    FEController[JS Controller]
    FEService[JS Service Layer]
    API[API Layer]
end

subgraph Backend
    Controller
    Service
    Repository
    Database
end

View --> FEController
FEController --> FEService
FEService --> API
API --> Controller
Controller --> Service
Service --> Repository
Repository --> Database


# SecureGate RBAC System

## Overview

SecureGate is a full-stack Role-Based Access Control (RBAC) system built with:

- FastAPI (Backend)
- PostgreSQL (Database)
- Plain JavaScript + Bootstrap (Frontend)
- Docker + GitHub Actions (CI/CD)

The system allows administrators to:
- Authenticate via JWT
- Assign roles to users
- Remove roles
- Enforce permission-based access
- View audit logs for denied actions

---

## Architecture

```mermaid
graph TD
Controller --> Service
Service --> Repository
Repository --> Database

<img width="1894" height="959" alt="Screenshot 2026-02-14 165752" src="https://github.com/user-attachments/assets/d0d84c01-8f66-4af6-aac1-e497eb34b0c9" />
<img width="1100" height="744" alt="Screenshot 2026-02-12 155712" src="https://github.com/user-attachments/assets/8e9e2383-d5e4-4bf8-ae3f-043b8bbc6b54" />
<img width="1408" height="837" alt="Screenshot 2026-02-12 170235" src="https://github.com/user-attachments/assets/92ba9aa3-2143-4538-bc04-39be719c9d9a" />
<img width="1894" height="959" alt="Screenshot 2026-02-14 165752" src="https://github.com/user-attachments/assets/c84cefa1-e20c-4e59-b92b-8116ba3af7bb" />
<img width="1897" height="939" alt="Screenshot 2026-02-14 165759" src="https://github.com/user-attachments/assets/0af26c26-dba7-4d60-8a27-3eff813428b0" />
<img width="1431" height="421" alt="Screenshot 2026-02-14 172211" src="https://github.com/user-attachments/assets/1e2da28e-ed68-4312-beab-f1ae4ec7f932" />
<img width="671" height="569" alt="Screenshot 2026-02-14 172745" src="https://github.com/user-attachments/assets/88094e31-ed7d-403c-aa8d-e8d5b324556b" />
<img width="1405" height="903" alt="Screenshot 2026-02-14 175047" src="https://github.com/user-attachments/assets/f342ad30-03d6-4236-bee1-c559f8fe2274" />
<img width="799" height="508" alt="Screenshot 2026-02-15 134543" src="https://github.com/user-attachments/assets/d5e8893b-3ce4-4bc4-986a-fe4a1cae50db" />








