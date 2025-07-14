// User types
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  bio?: string;
  profile_picture?: string;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  user: User;
  token: string;
  message: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  password: string;
  password_confirm: string;
  bio?: string;
  profile_picture?: File;
}

// Category types
export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  created_at: string;
  updated_at: string;
}

// Blog post types
export interface BlogPost {
  id: number;
  title: string;
  slug: string;
  description: string;
  content: string;
  image?: string;
  author: User;
  category: Category;
  is_published: boolean;
  is_liked?: boolean;
  likes_count: number;
  comments_count: number;
  created_at: string;
  updated_at: string;
}

export interface BlogPostCreate {
  title: string;
  description: string;
  content: string;
  image?: File;
  category: number;
  is_published: boolean;
}

export interface BlogPostList {
  count: number;
  next: string | null;
  previous: string | null;
  results: BlogPost[];
}

// Comment types
export interface Comment {
  id: number;
  author: User;
  blog_post: number;
  content: string;
  parent?: number;
  replies_count: number;
  replies: Comment[];
  created_at: string;
  updated_at: string;
}

export interface CommentCreate {
  content: string;
  blog_post: number;
  parent?: number;
}

// Like types
export interface Like {
  id: number;
  user: User;
  blog_post: number;
  created_at: string;
}

export interface LikeResponse {
  message: string;
  liked: boolean;
  likes_count: number;
}

// API Error type
export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
}

// Pagination types
export interface PaginationParams {
  page?: number;
  search?: string;
  ordering?: string;
  category?: string;
  author?: string;
}
