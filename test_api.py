#!/usr/bin/env python
"""
Test script for Blog API endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_user_registration():
    """Test user registration"""
    print("Testing user registration...")
    
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get('token')

def test_user_login():
    """Test user login"""
    print("\nTesting user login...")
    
    data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get('token')

def test_create_category(token):
    """Test creating a category"""
    print("\nTesting category creation...")
    
    headers = {"Authorization": f"Token {token}"}
    data = {
        "name": "Technology",
        "description": "Posts about technology"
    }
    
    response = requests.post(f"{BASE_URL}/blog/categories/", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get('id')

def test_create_blog_post(token, category_id):
    """Test creating a blog post"""
    print("\nTesting blog post creation...")
    
    headers = {"Authorization": f"Token {token}"}
    data = {
        "title": "My First Blog Post",
        "description": "This is a test blog post",
        "content": "This is the full content of my first blog post. It's quite interesting!",
        "category": category_id,
        "is_published": True
    }
    
    response = requests.post(f"{BASE_URL}/blog/posts/create/", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get('blog_post', {}).get('slug')

def test_list_blog_posts():
    """Test listing blog posts"""
    print("\nTesting blog post listing...")
    
    response = requests.get(f"{BASE_URL}/blog/posts/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_like_blog_post(token, post_slug):
    """Test liking a blog post"""
    print("\nTesting blog post like...")
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(f"{BASE_URL}/blog/posts/{post_slug}/like/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_create_comment(token, post_slug):
    """Test creating a comment"""
    print("\nTesting comment creation...")
    
    headers = {"Authorization": f"Token {token}"}
    data = {
        "content": "This is a great blog post!"
    }
    
    response = requests.post(f"{BASE_URL}/blog/posts/{post_slug}/comments/", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def main():
    """Run all tests"""
    print("Starting Blog API Tests\n")
    
    try:
        # Test user registration
        token = test_user_registration()
        
        if not token:
            # If registration fails, try login
            token = test_user_login()
        
        if token:
            # Test category creation
            category_id = test_create_category(token)
            
            if category_id:
                # Test blog post creation
                post_slug = test_create_blog_post(token, category_id)
                
                # Test blog post listing
                test_list_blog_posts()
                
                if post_slug:
                    # Test liking a post
                    test_like_blog_post(token, post_slug)
                    
                    # Test creating a comment
                    test_create_comment(token, post_slug)
            
            print("\nAll tests completed!")
        else:
            print("Could not obtain authentication token. Tests stopped.")
    
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure Django server is running.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
