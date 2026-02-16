#!/usr/bin/env python3
"""
Test script for SecureGate RBAC API
Tests all implemented endpoints with proper error handling
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

class RBACTester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.admin_token = None
        self.user_token = None
        self.session = requests.Session()
    
    def print_result(self, test_name: str, success: bool, message: str = ""):
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"\n{status}: {test_name}")
        if message:
            print(f"  └─ {message}")
    
    def print_response(self, response: requests.Response):
        try:
            print(f"  Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"  Response: {response.text}")
    
    def test_login(self, username: str, password: str) -> bool:
        """Test login endpoint"""
        print(f"\n{'='*60}")
        print(f"Testing: POST /auth/login - {username}")
        print(f"{'='*60}")
        
        payload = {
            "username": username,
            "password": password
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json=payload
            )
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                token = data.get("token")
                if username == "admin":
                    self.admin_token = token
                    print(f"✓ Admin token obtained")
                else:
                    self.user_token = token
                    print(f"✓ User token obtained")
                
                self.print_result(f"Login as {username}", success)
                self.print_response(response)
            else:
                self.print_result(f"Login as {username}", success, f"Status {response.status_code}")
                self.print_response(response)
            
            return success
        except Exception as e:
            self.print_result(f"Login as {username}", False, str(e))
            return False
    
    def test_get_resource(self, token: str, username: str) -> bool:
        """Test GET /resource endpoint"""
        print(f"\n{'='*60}")
        print(f"Testing: GET /resource - {username}")
        print(f"{'='*60}")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = self.session.get(
                f"{self.base_url}/resource",
                headers=headers
            )
            
            success = response.status_code == 200
            self.print_result(f"Access /resource as {username}", success, f"Status {response.status_code}")
            self.print_response(response)
            
            return success
        except Exception as e:
            self.print_result(f"Access /resource as {username}", False, str(e))
            return False
    
    def test_unauthorized_resource_access(self):
        """Test accessing resource without token"""
        print(f"\n{'='*60}")
        print(f"Testing: GET /resource - Without Token (Should Fail)")
        print(f"{'='*60}")
        
        try:
            response = self.session.get(
                f"{self.base_url}/resource"
            )
            
            success = response.status_code == 422 or response.status_code == 401
            message = f"Expected 401/422, got {response.status_code}"
            self.print_result("Unauthorized access without token", success, message)
            self.print_response(response)
            
            return success
        except Exception as e:
            self.print_result("Unauthorized access without token", False, str(e))
            return False
    
    def test_assign_role(self, admin_token: str, username: str = "user", role_id: int = 4) -> bool:
        """Test POST /admin/assign-role endpoint"""
        print(f"\n{'='*60}")
        print(f"Testing: POST /admin/assign-role - Admin Only")
        print(f"{'='*60}")
        
        headers = {
            "Authorization": f"Bearer {admin_token}",
            "Content-Type": "application/json"
        }
        
        # Assign the "user" account to a role (role_id=4 should be "User")
        payload = {
            "user_id": 6,  # Based on fresh setup_db.py, the regular user should have ID 6
            "role_id": role_id  # Role ID 4 should be "User" after latest setup
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/admin/assign-role",
                json=payload,
                headers=headers
            )
            
            success = response.status_code == 200
            self.print_result(f"Assign role to user {payload['user_id']}", success, f"Status {response.status_code}")
            self.print_response(response)
            
            return success
        except Exception as e:
            self.print_result(f"Assign role to user {payload['user_id']}", False, str(e))
            return False
    
    def test_unauthorized_assign_role(self, user_token: str):
        """Test assigning role without ADMIN permission"""
        print(f"\n{'='*60}")
        print(f"Testing: POST /admin/assign-role - Regular User (Should Fail)")
        print(f"{'='*60}")
        
        headers = {
            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "user_id": 5,  # Try to assign to admin user, use valid user ID from fresh setup
            "role_id": 1
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/admin/assign-role",
                json=payload,
                headers=headers
            )
            
            success = response.status_code == 403
            message = f"Expected 403, got {response.status_code}"
            self.print_result("Unauthorized assign-role (regular user)", success, message)
            self.print_response(response)
            
            return success
        except Exception as e:
            self.print_result("Unauthorized assign-role (regular user)", False, str(e))
            return False
    
    def run_full_test_suite(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("SECUREGATE RBAC - FULL TEST SUITE")
        print("="*60)
        
        results = []
        
        # Test login
        results.append(("Login as admin", self.test_login("admin", "admin123")))
        results.append(("Login as user", self.test_login("user", "user123")))
        
        # Wait a moment
        import time
        time.sleep(1)
        
        # Test resource access
        results.append(("Admin access /resource", self.test_get_resource(self.admin_token, "admin")))
        results.append(("User access /resource", self.test_get_resource(self.user_token, "user")))
        results.append(("Unauthorized resource access", self.test_unauthorized_resource_access()))
        
        # Test role assignment (test unauthorized BEFORE authorized to avoid permission pollution)
        results.append(("User unauthorized assign role", self.test_unauthorized_assign_role(self.user_token)))
        results.append(("Admin assign role", self.test_assign_role(self.admin_token)))
        
        # Print summary
        print(f"\n\n{'='*60}")
        print("TEST SUMMARY")
        print(f"{'='*60}")
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✓" if result else "✗"
            print(f"{status} {test_name}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        print(f"{'='*60}\n")
        
        return passed == total

if __name__ == "__main__":
    print("Starting SecureGate RBAC API Tests...")
    print("Make sure the server is running: python serve.py\n")
    
    tester = RBACTester()
    success = tester.run_full_test_suite()
    
    if success:
        print("✓ ALL TESTS PASSED!")
    else:
        print("✗ SOME TESTS FAILED - Check output above")
