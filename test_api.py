#!/usr/bin/env python3
"""
Simple API test script for the Hex Puzzle Game
"""
import requests
import json

BASE_URL = "http://localhost:5001"

def test_api():
    """Test basic API functionality"""
    print("Testing Hex Puzzle Game API...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ Server is running (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("✗ Server is not running. Please start the server first.")
        return False
    
    # Test 2: Test registration
    test_user = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/register", json=test_user)
        if response.status_code == 200:
            print("✓ User registration successful")
        else:
            print(f"✗ User registration failed: {response.status_code}")
            data = response.json()
            print(f"  Error: {data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"✗ Registration test failed: {e}")
    
    # Test 3: Test login
    try:
        response = requests.post(f"{BASE_URL}/api/login", json=test_user)
        if response.status_code == 200:
            print("✓ User login successful")
            data = response.json()
            print(f"  User ID: {data.get('user_id')}")
            print(f"  Current Chapter: {data.get('current_chapter')}")
        else:
            print(f"✗ User login failed: {response.status_code}")
            data = response.json()
            print(f"  Error: {data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"✗ Login test failed: {e}")
    
    print("\nAPI test completed!")
    return True

if __name__ == '__main__':
    test_api() 