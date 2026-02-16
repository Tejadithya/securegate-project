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
