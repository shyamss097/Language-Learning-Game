from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/', home, name='home'),
    path('exercises/<int:language_id>/', exercises, name='exercises'),
    path('user/profile/', user_profile, name='user_profile'),
    path('user/settings/', user_settings, name='user_settings'),
    path('leaderboard/<int:language_id>/', leaderboard, name='leaderboard'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('score_page/', score_page, name='score_page'),
    # Add more URL patterns as needed
]
