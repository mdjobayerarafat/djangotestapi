from rest_framework import serializers
from blog.models import Category, BlogPost, Like, Comment
from authentication.serializers.user_serializers import UserProfileSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')


class BlogPostListSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost list view"""
    author = UserProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    
    class Meta:
        model = BlogPost
        fields = (
            'id', 'title', 'slug', 'description', 'image', 
            'author', 'category', 'is_published', 'likes_count', 
            'comments_count', 'created_at', 'updated_at'
        )


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost detail view"""
    author = UserProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    
    class Meta:
        model = BlogPost
        fields = (
            'id', 'title', 'slug', 'description', 'content', 'image',
            'author', 'category', 'is_published', 'likes_count',
            'comments_count', 'created_at', 'updated_at'
        )


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating BlogPost"""
    
    class Meta:
        model = BlogPost
        fields = (
            'title', 'description', 'content', 'image', 
            'category', 'is_published'
        )
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for Like model"""
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ('id', 'user', 'blog_post', 'created_at')
        read_only_fields = ('id', 'created_at')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    user = UserProfileSerializer(read_only=True)
    replies_count = serializers.ReadOnlyField()
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = (
            'id', 'user', 'blog_post', 'content', 'parent',
            'replies_count', 'replies', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Comment"""
    
    class Meta:
        model = Comment
        fields = ('content', 'blog_post', 'parent')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
