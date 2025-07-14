from django.contrib import admin
from blog.models import Category, BlogPost, Like, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin"""
    list_display = ('name', 'slug', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Blog Post admin"""
    list_display = ('title', 'author', 'category', 'is_published', 'created_at')
    list_filter = ('is_published', 'category', 'created_at', 'author')
    search_fields = ('title', 'description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'likes_count', 'comments_count')
    raw_id_fields = ('author', 'category')
    
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'description', 'content', 'image')}),
        ('Publishing', {'fields': ('author', 'category', 'is_published')}),
        ('Metadata', {'fields': ('created_at', 'updated_at', 'likes_count', 'comments_count')}),
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Like admin"""
    list_display = ('user', 'blog_post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'blog_post__title')
    raw_id_fields = ('user', 'blog_post')
    readonly_fields = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin"""
    list_display = ('user', 'blog_post', 'parent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'blog_post__title', 'content')
    raw_id_fields = ('user', 'blog_post', 'parent')
    readonly_fields = ('created_at', 'updated_at', 'replies_count')
    
    fieldsets = (
        (None, {'fields': ('user', 'blog_post', 'content', 'parent')}),
        ('Metadata', {'fields': ('created_at', 'updated_at', 'replies_count')}),
    )
