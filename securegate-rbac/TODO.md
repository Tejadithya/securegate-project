# TODO List for SecureGate RBAC Project Fixes

## 1. Update requirements.txt with dependencies
- [x] Add FastAPI, Uvicorn, SQLAlchemy, psycopg2-binary, python-jose[cryptography], pydantic

## 2. Create app/main.py
- [x] Initialize FastAPI app
- [x] Include routers (auth, admin)
- [x] Create database tables on startup

## 3. Update app/routes/auth_routes.py
- [x] Use get_db dependency instead of creating sessions directly
- [x] Handle token from Authorization header

## 4. Update app/routes/admin_routes.py
- [x] Use get_db dependency instead of creating sessions directly
- [x] Handle token from Authorization header

## 5. Fix app/middleware..py
- [x] Update require_permission to extract token from Authorization header

## 6. Create schemas in app/schemas/
- [x] Define Pydantic models for requests/responses (LoginRequest, AssignRoleRequest, etc.)

## 7. Implement repositories
- [x] Basic implementations in app/repositories/user_repo.py for user operations
- [x] Basic implementations in app/repositories/role_repo.py for role operations

## 8. Implement services
- [x] Basic implementations in app/services/auth_service.py for auth logic
- [x] Basic implementations in app/services/rbac_service.py for RBAC logic

## 9. Update tests/test_authorization.py
- [x] Add proper test setup (fixtures for client, db, tokens)
- [x] Ensure tests can run

## 10. Ensure database tables are created
- [ ] Add Base.metadata.create_all in main.py or database.py
