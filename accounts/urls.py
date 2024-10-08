from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('change_password/', views.change_password, name='change_password'),
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='forgot_password/password_reset.html'), 
         name='password_reset'),
    path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='forgot_password/password_reset_done.html'), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='forgot_password/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='forgot_password/password_reset_complete.html'), 
        name='password_reset_complete'),
]
