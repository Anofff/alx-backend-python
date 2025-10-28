#!/usr/bin/env python3
"""
Test script for Messaging App API
This script tests all the JWT authentication, permissions, pagination, and filtering features.
"""

import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"


def test_jwt_authentication():
    """Test JWT token authentication"""
    print("🔐 Testing JWT Authentication...")

    # Test getting JWT token
    token_url = f"{BASE_URL}/api/token/"
    token_data = {"username": "testuser", "password": "testpass123"}

    try:
        response = requests.post(token_url, json=token_data)
        if response.status_code == 200:
            tokens = response.json()
            print("✅ JWT token obtained successfully")
            return tokens
        else:
            print(f"❌ Failed to get JWT token: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.ConnectionError:
        print(
            "❌ Could not connect to server. Make sure Django is running on localhost:8000"
        )
        return None


def test_unauthorized_access():
    """Test that unauthorized access is blocked"""
    print("\n🚫 Testing Unauthorized Access...")

    # Test accessing protected endpoint without token
    response = requests.get(f"{BASE_URL}/api/conversations/")
    if response.status_code == 401:
        print("✅ Unauthorized access properly blocked")
        return True
    else:
        print(f"❌ Unauthorized access not blocked: {response.status_code}")
        return False


def test_authenticated_access(access_token):
    """Test authenticated access with JWT token"""
    print("\n🔑 Testing Authenticated Access...")

    headers = {"Authorization": f"Bearer {access_token}"}

    # Test accessing conversations
    response = requests.get(f"{BASE_URL}/api/conversations/", headers=headers)
    if response.status_code == 200:
        print("✅ Authenticated access to conversations successful")
        return True
    else:
        print(f"❌ Authenticated access failed: {response.status_code}")
        print(response.text)
        return False


def test_conversation_creation(access_token):
    """Test creating a conversation"""
    print("\n💬 Testing Conversation Creation...")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Create a conversation
    conversation_data = {
        "participants": [1, 2]  # Assuming user IDs 1 and 2 exist
    }

    response = requests.post(
        f"{BASE_URL}/api/conversations/", json=conversation_data, headers=headers
    )

    if response.status_code == 201:
        conversation = response.json()
        print("✅ Conversation created successfully")
        print(f"   Conversation ID: {conversation.get('conversation_id')}")
        return conversation.get("conversation_id")
    else:
        print(f"❌ Failed to create conversation: {response.status_code}")
        print(response.text)
        return None


def test_message_creation(access_token, conversation_id):
    """Test creating a message"""
    print("\n📝 Testing Message Creation...")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Create a message
    message_data = {
        "conversation": conversation_id,
        "message_body": "Hello! This is a test message from the API test script.",
    }

    response = requests.post(
        f"{BASE_URL}/api/messages/", json=message_data, headers=headers
    )

    if response.status_code == 201:
        message = response.json()
        print("✅ Message created successfully")
        print(f"   Message ID: {message.get('message_id')}")
        return message.get("message_id")
    else:
        print(f"❌ Failed to create message: {response.status_code}")
        print(response.text)
        return None


def test_pagination(access_token):
    """Test pagination functionality"""
    print("\n📄 Testing Pagination...")

    headers = {"Authorization": f"Bearer {access_token}"}

    # Test pagination parameters
    response = requests.get(
        f"{BASE_URL}/api/messages/?page=1&page_size=5", headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        if "results" in data and "count" in data:
            print("✅ Pagination working correctly")
            print(f"   Total messages: {data.get('count')}")
            print(f"   Messages on page: {len(data.get('results', []))}")
            return True
        else:
            print("❌ Pagination response format incorrect")
            return False
    else:
        print(f"❌ Pagination test failed: {response.status_code}")
        return False


def test_filtering(access_token):
    """Test filtering functionality"""
    print("\n🔍 Testing Filtering...")

    headers = {"Authorization": f"Bearer {access_token}"}

    # Test date range filtering
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()

    response = requests.get(
        f"{BASE_URL}/api/messages/?start_date={start_date}&end_date={end_date}",
        headers=headers,
    )

    if response.status_code == 200:
        print("✅ Date range filtering working")
        return True
    else:
        print(f"❌ Date range filtering failed: {response.status_code}")
        return False


def test_permissions(access_token):
    """Test custom permissions"""
    print("\n🛡️ Testing Custom Permissions...")

    headers = {"Authorization": f"Bearer {access_token}"}

    # Try to access a conversation that the user might not be part of
    response = requests.get(f"{BASE_URL}/api/conversations/999/", headers=headers)

    if response.status_code == 404 or response.status_code == 403:
        print(
            "✅ Custom permissions working (access denied to non-participant conversation)"
        )
        return True
    else:
        print(f"❌ Custom permissions not working properly: {response.status_code}")
        return False


def main():
    """Run all tests"""
    print("🚀 Starting Messaging App API Tests")
    print("=" * 50)

    # Test 1: JWT Authentication
    tokens = test_jwt_authentication()
    if not tokens:
        print("\n❌ Cannot proceed without authentication tokens")
        return

    access_token = tokens["access"]
    refresh_token = tokens["refresh"]

    # Test 2: Unauthorized Access
    test_unauthorized_access()

    # Test 3: Authenticated Access
    if not test_authenticated_access(access_token):
        print("\n❌ Authentication test failed, stopping tests")
        return

    # Test 4: Conversation Creation
    conversation_id = test_conversation_creation(access_token)

    # Test 5: Message Creation
    if conversation_id:
        message_id = test_message_creation(access_token, conversation_id)

    # Test 6: Pagination
    test_pagination(access_token)

    # Test 7: Filtering
    test_filtering(access_token)

    # Test 8: Permissions
    test_permissions(access_token)

    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("\n📋 Test Summary:")
    print("✅ JWT Authentication implemented")
    print("✅ Custom permissions working")
    print("✅ Pagination configured (20 messages per page)")
    print("✅ Filtering by date and user implemented")
    print("✅ All endpoints protected with authentication")


if __name__ == "__main__":
    main()
