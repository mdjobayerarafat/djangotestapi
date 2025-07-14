# Blog API Documentation

## Overview
This is a Django REST API for a blog website with user authentication, blog posts, categories, likes, and comments.

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login  
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Categories
- `GET /api/blog/categories/` - List all categories
- `POST /api/blog/categories/` - Create new category (authenticated)
- `GET /api/blog/categories/<slug>/` - Get category details
- `PUT /api/blog/categories/<slug>/` - Update category (authenticated)
- `DELETE /api/blog/categories/<slug>/` - Delete category (authenticated)

### Blog Posts
- `GET /api/blog/posts/` - List all published posts
- `POST /api/blog/posts/create/` - Create new post (authenticated)
- `GET /api/blog/posts/<slug>/` - Get post details
- `PUT /api/blog/posts/<slug>/update/` - Update post (author only)
- `DELETE /api/blog/posts/<slug>/delete/` - Delete post (author only)
- `GET /api/blog/my-posts/` - List user's posts (authenticated)
- `POST /api/blog/posts/<slug>/like/` - Toggle like on post (authenticated)

### Comments
- `GET /api/blog/posts/<slug>/comments/` - List post comments
- `POST /api/blog/posts/<slug>/comments/` - Create comment (authenticated)
- `GET /api/blog/comments/<id>/` - Get comment details
- `PUT /api/blog/comments/<id>/` - Update comment (author only)
- `DELETE /api/blog/comments/<id>/` - Delete comment (author only)

## Authentication
The API uses Token-based authentication. After login/registration, include the token in the Authorization header:
```
Authorization: Token <your-token-here>
```

## Example Usage

### Register a new user
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### Create a blog post
```bash
curl -X POST http://localhost:8000/api/blog/posts/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <your-token>" \
  -d '{
    "title": "My First Blog Post",
    "description": "This is a test blog post",
    "content": "This is the full content of my blog post...",
    "category": 1,
    "is_published": true
  }'
```

## Features
- User registration and authentication
- Blog post CRUD operations
- Category management
- Like system for posts
- Hierarchical comments system
- Image upload for posts and user profiles
- Search and filtering
- Pagination
- Clean code architecture with separate serializers and views
