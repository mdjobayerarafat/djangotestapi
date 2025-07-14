from django.urls import path
from blog.views.blog_views import (
    CategoryListCreateView,
    CategoryDetailView,
    BlogPostListView,
    BlogPostCreateView,
    BlogPostDetailView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    UserBlogPostsView,
    toggle_like,
    CommentListCreateView,
    CommentDetailView
)

app_name = 'blog'

urlpatterns = [
    # Category URLs
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Blog Post URLs
    path('posts/', BlogPostListView.as_view(), name='post-list'),
    path('posts/create/', BlogPostCreateView.as_view(), name='post-create'),
    path('posts/<slug:slug>/', BlogPostDetailView.as_view(), name='post-detail'),
    path('posts/<slug:slug>/update/', BlogPostUpdateView.as_view(), name='post-update'),
    path('posts/<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='post-delete'),
    path('posts/<slug:slug>/like/', toggle_like, name='post-like'),
    
    # User's posts
    path('my-posts/', UserBlogPostsView.as_view(), name='user-posts'),
    
    # Comment URLs
    path('posts/<slug:slug>/comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
