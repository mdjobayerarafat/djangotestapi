from django.urls import path
from authentication.views.auth_views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserProfileView
)

app_name = 'authentication'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
