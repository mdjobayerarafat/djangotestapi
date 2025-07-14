'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import apiClient from '@/lib/api';
import { BlogPost, Comment, CommentCreate } from '@/types';
import { handleApiError } from '@/lib/utils';
import { Heart, MessageCircle, Calendar, User, Edit, Trash2, Reply, Send } from 'lucide-react';
import Link from 'next/link';
import Image from 'next/image';
import { useForm } from 'react-hook-form';

export default function BlogDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { user, isAuthenticated } = useAuth();
  const [post, setPost] = useState<BlogPost | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isLiked, setIsLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [commentError, setCommentError] = useState<string | null>(null);
  const [isSubmittingComment, setIsSubmittingComment] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm<CommentCreate>();

  useEffect(() => {
    if (params.slug) {
      loadPost();
      loadComments();
    }
  }, [params.slug]);

  const loadPost = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const postData = await apiClient.getBlogPost(params.slug as string);
      setPost(postData);
      setIsLiked(postData.is_liked || false);
      setLikesCount(postData.likes_count);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setIsLoading(false);
    }
  };

  const loadComments = async () => {
    try {
      const commentsData = await apiClient.getComments(params.slug as string);
      // Ensure comments is always an array
      setComments(Array.isArray(commentsData) ? commentsData : []);
    } catch (err) {
      console.error('Error loading comments:', err);
      setComments([]); // Set empty array on error
    }
  };

  const handleLike = async () => {
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    try {
      const response = await apiClient.toggleLike(params.slug as string);
      setIsLiked(response.liked);
      setLikesCount(response.likes_count);
    } catch (err) {
      console.error('Error toggling like:', err);
    }
  };

  const handleCommentSubmit = async (data: CommentCreate) => {
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    try {
      setIsSubmittingComment(true);
      setCommentError(null);
      const response = await apiClient.createComment(params.slug as string, data);
      setComments(prev => [...prev, response.comment]);
      reset();
    } catch (err) {
      setCommentError(handleApiError(err));
    } finally {
      setIsSubmittingComment(false);
    }
  };

  const handleDeleteComment = async (commentId: number) => {
    if (!confirm('Are you sure you want to delete this comment?')) return;

    try {
      await apiClient.deleteComment(commentId);
      setComments(prev => prev.filter(comment => comment.id !== commentId));
    } catch (err) {
      console.error('Error deleting comment:', err);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded mb-4"></div>
          <div className="h-64 bg-gray-200 rounded mb-6"></div>
          <div className="h-4 bg-gray-200 rounded mb-2"></div>
          <div className="h-4 bg-gray-200 rounded mb-2 w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded mb-8 w-1/2"></div>
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Post Not Found</h1>
          <p className="text-gray-600 mb-8">{error || 'The blog post you are looking for does not exist.'}</p>
          <Link
            href="/blog"
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Back to Blog
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <article className="bg-white rounded-lg shadow-lg overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
              {post.category?.name || 'Uncategorized'}
            </span>
            {user && user.id === post.author.id && (
              <div className="flex items-center space-x-2">
                <Link
                  href={`/blog/${post.slug}/edit`}
                  className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-full"
                  title="Edit post"
                >
                  <Edit className="h-5 w-5" />
                </Link>
                <button
                  onClick={() => {
                    if (confirm('Are you sure you want to delete this post?')) {
                      // Handle delete
                    }
                  }}
                  className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-full"
                  title="Delete post"
                >
                  <Trash2 className="h-5 w-5" />
                </button>
              </div>
            )}
          </div>
          
          <h1 className="text-3xl font-bold text-gray-900 mb-4">{post.title}</h1>
          
          <div className="flex items-center space-x-4 text-sm text-gray-600">
            <div className="flex items-center">
              <User className="h-4 w-4 mr-2" />
              {post.author.first_name} {post.author.last_name}
            </div>
            <div className="flex items-center">
              <Calendar className="h-4 w-4 mr-2" />
              {formatDate(post.created_at)}
            </div>
          </div>
        </div>

        {/* Image */}
        {post.image && (
          <div className="px-6 py-4">
            <Image
              src={post.image}
              alt={post.title}
              width={800}
              height={400}
              className="w-full h-96 object-cover rounded-lg"
            />
          </div>
        )}

        {/* Content */}
        <div className="px-6 py-4">
          <div className="prose max-w-none">
            <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
              {post.description}
            </p>
          </div>
        </div>

        {/* Actions */}
        <div className="px-6 py-4 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={handleLike}
                className={`flex items-center space-x-2 px-4 py-2 rounded-full border transition-colors ${
                  isLiked
                    ? 'bg-red-50 border-red-200 text-red-600'
                    : 'bg-gray-50 border-gray-200 text-gray-600 hover:bg-red-50 hover:border-red-200 hover:text-red-600'
                }`}
              >
                <Heart className={`h-5 w-5 ${isLiked ? 'fill-current' : ''}`} />
                <span>{likesCount}</span>
              </button>
              <div className="flex items-center space-x-2 text-gray-600">
                <MessageCircle className="h-5 w-5" />
                <span>{comments.length} comments</span>
              </div>
            </div>
          </div>
        </div>
      </article>

      {/* Comments Section */}
      <div className="mt-8 bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Comments ({comments.length})</h3>
        </div>

        {/* Comment Form */}
        {isAuthenticated ? (
          <div className="px-6 py-4 border-b border-gray-200">
            <form onSubmit={handleSubmit(handleCommentSubmit)} className="space-y-4">
              {commentError && (
                <div className="p-3 bg-red-50 border border-red-200 text-red-600 rounded-md">
                  {commentError}
                </div>
              )}
              <div>
                <textarea
                  {...register('content', { required: 'Comment content is required' })}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Write a comment..."
                />
                {errors.content && (
                  <p className="mt-1 text-sm text-red-600">{errors.content.message}</p>
                )}
              </div>
              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={isSubmittingComment}
                  className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Send className="h-4 w-4 mr-2" />
                  {isSubmittingComment ? 'Posting...' : 'Post Comment'}
                </button>
              </div>
            </form>
          </div>
        ) : (
          <div className="px-6 py-4 border-b border-gray-200 text-center">
            <p className="text-gray-600">
              <Link href="/auth/login" className="text-blue-600 hover:text-blue-800">
                Sign in
              </Link>{' '}
              to leave a comment
            </p>
          </div>
        )}

        {/* Comments List */}
        <div className="divide-y divide-gray-200">
          {comments.length === 0 ? (
            <div className="px-6 py-8 text-center">
              <MessageCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No comments yet. Be the first to comment!</p>
            </div>
          ) : (
            comments.map((comment) => (
              <div key={comment.id} className="px-6 py-4">
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <div className="h-10 w-10 bg-gray-300 rounded-full flex items-center justify-center">
                      <User className="h-6 w-6 text-gray-600" />
                    </div>
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <h4 className="font-medium text-gray-900">
                        {comment.author.first_name} {comment.author.last_name}
                      </h4>
                      <span className="text-sm text-gray-500">
                        {formatDate(comment.created_at)}
                      </span>
                    </div>
                    <p className="text-gray-700">{comment.content}</p>
                    {user && user.id === comment.author.id && (
                      <div className="mt-2 flex items-center space-x-2">
                        <button
                          onClick={() => handleDeleteComment(comment.id)}
                          className="text-sm text-red-600 hover:text-red-800"
                        >
                          Delete
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
