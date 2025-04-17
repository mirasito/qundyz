from django.urls import path
from .views import register, UserLoginView, profile_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(next_page='user_login'), name='logout'),
    path('profile/', profile_view, name='user_profile'),
]