from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from blog.models import Category, BlogPost, Like, Comment
from blog.serializers.blog_serializers import (
    CategorySerializer,
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    BlogPostCreateUpdateSerializer,
    LikeSerializer,
    CommentSerializer,
    CommentCreateUpdateSerializer
)


class CategoryListCreateView(generics.ListCreateAPIView):
    """View for listing and creating categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for category detail, update, and delete"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class BlogPostListView(generics.ListAPIView):
    """View for listing blog posts"""
    serializer_class = BlogPostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True)
        category = self.request.query_params.get('category')
        author = self.request.query_params.get('author')
        
        if category:
            queryset = queryset.filter(category__slug=category)
        if author:
            queryset = queryset.filter(author__username=author)
        
        return queryset


class BlogPostCreateView(generics.CreateAPIView):
    """View for creating blog posts"""
    serializer_class = BlogPostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blog_post = serializer.save()
        
        return Response({
            'blog_post': BlogPostDetailSerializer(blog_post).data,
            'message': 'Blog post created successfully'
        }, status=status.HTTP_201_CREATED)


class BlogPostDetailView(generics.RetrieveAPIView):
    """View for blog post detail"""
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class BlogPostUpdateView(generics.UpdateAPIView):
    """View for updating blog posts"""
    serializer_class = BlogPostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'blog_post': BlogPostDetailSerializer(instance).data,
            'message': 'Blog post updated successfully'
        }, status=status.HTTP_200_OK)


class BlogPostDeleteView(generics.DestroyAPIView):
    """View for deleting blog posts"""
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Blog post deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class UserBlogPostsView(generics.ListAPIView):
    """View for listing user's blog posts"""
    serializer_class = BlogPostListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, slug):
    """Toggle like on a blog post"""
    blog_post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    like, created = Like.objects.get_or_create(
        user=request.user,
        blog_post=blog_post
    )
    
    if not created:
        like.delete()
        return Response({
            'message': 'Like removed',
            'liked': False,
            'likes_count': blog_post.likes_count
        }, status=status.HTTP_200_OK)
    
    return Response({
        'message': 'Post liked',
        'liked': True,
        'likes_count': blog_post.likes_count
    }, status=status.HTTP_201_CREATED)


class CommentListCreateView(generics.ListCreateAPIView):
    """View for listing and creating comments"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        blog_post_slug = self.kwargs.get('slug')
        blog_post = get_object_or_404(BlogPost, slug=blog_post_slug, is_published=True)
        return Comment.objects.filter(blog_post=blog_post, parent=None)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateUpdateSerializer
        return CommentSerializer
    
    def create(self, request, *args, **kwargs):
        blog_post_slug = self.kwargs.get('slug')
        blog_post = get_object_or_404(BlogPost, slug=blog_post_slug, is_published=True)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(blog_post=blog_post)
        
        return Response({
            'comment': CommentSerializer(comment).data,
            'message': 'Comment created successfully'
        }, status=status.HTTP_201_CREATED)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for comment detail, update, and delete"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return Comment.objects.filter(user=self.request.user)
        return Comment.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CommentCreateUpdateSerializer
        return CommentSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'comment': CommentSerializer(instance).data,
            'message': 'Comment updated successfully'
        }, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Comment deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
