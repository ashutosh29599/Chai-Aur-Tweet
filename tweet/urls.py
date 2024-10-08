from django.urls import path

from . import views

urlpatterns = [
    path('', views.tweet_home, name='tweet_home'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),   
    path('search/', views.tweet_search, name='tweet_search'),
    path('users/', views.users, name='users'),
] 
