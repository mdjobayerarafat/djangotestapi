# Django Blog API

A comprehensive Django REST API for a blog website with user authentication, blog posts, categories, likes, and comments system.

## Features

- ✅ User authentication (registration, login, logout)
- ✅ User profiles with image upload
- ✅ Blog posts with CRUD operations
- ✅ Categories management
- ✅ Like system for blog posts
- ✅ Hierarchical comments system
- ✅ Image upload for posts and profiles
- ✅ Search and filtering
- ✅ Pagination
- ✅ Clean code architecture
- ✅ Comprehensive API endpoints

## Project Structure

```
blog_api/
├── blog_api/                 # Main project directory
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── authentication/          # Authentication app
│   ├── models.py           # Custom User model
│   ├── admin.py            # User admin configuration
│   ├── views/              # Authentication views
│   │   └── auth_views.py
│   ├── serializers/        # Authentication serializers
│   │   └── user_serializers.py
│   └── urls.py             # Authentication URLs
├── blog/                   # Blog app
│   ├── models.py           # Blog models (BlogPost, Category, Like, Comment)
│   ├── admin.py            # Blog admin configuration
│   ├── views/              # Blog views
│   │   └── blog_views.py
│   ├── serializers/        # Blog serializers
│   │   └── blog_serializers.py
│   └── urls.py             # Blog URLs
├── media/                  # Media files (uploaded images)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── .gitignore             # Git ignore file
├── manage.py              # Django management script
├── test_api.py            # API test script
└── API_DOCUMENTATION.md   # API documentation
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd blog_api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Categories
- `GET /api/blog/categories/` - List all categories
- `POST /api/blog/categories/` - Create new category
- `GET /api/blog/categories/<slug>/` - Get category details
- `PUT /api/blog/categories/<slug>/` - Update category
- `DELETE /api/blog/categories/<slug>/` - Delete category

### Blog Posts
- `GET /api/blog/posts/` - List all published posts
- `POST /api/blog/posts/create/` - Create new post
- `GET /api/blog/posts/<slug>/` - Get post details
- `PUT /api/blog/posts/<slug>/update/` - Update post
- `DELETE /api/blog/posts/<slug>/delete/` - Delete post
- `GET /api/blog/my-posts/` - List user's posts
- `POST /api/blog/posts/<slug>/like/` - Toggle like on post

### Comments
- `GET /api/blog/posts/<slug>/comments/` - List post comments
- `POST /api/blog/posts/<slug>/comments/` - Create comment
- `GET /api/blog/comments/<id>/` - Get comment details
- `PUT /api/blog/comments/<id>/` - Update comment
- `DELETE /api/blog/comments/<id>/` - Delete comment

## Testing

Run the test script to verify all endpoints:
```bash
python test_api.py
```

## Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/` to manage:
- Users
- Categories
- Blog Posts
- Comments
- Likes

## Clean Architecture

The project follows clean architecture principles:

1. **Separation of Concerns**: Each app has a specific responsibility
2. **Layered Architecture**: Models, Serializers, Views, and URLs are separated
3. **Dependency Injection**: Services are injected through Django's built-in mechanisms
4. **Interface Segregation**: Specific serializers for different operations
5. **Single Responsibility**: Each class has a single, well-defined purpose

## Technologies Used

- Django 5.2.4
- Django REST Framework 3.16.0
- Python 3.13
- SQLite (default, can be changed to PostgreSQL/MySQL)
- Pillow (for image handling)
- python-decouple (for environment variables)
- django-cors-headers (for CORS support)

## License

This project is licensed under the MIT License.
