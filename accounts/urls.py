from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('author/<str:username>/', views.user_profile, name='profile'),
    # login / logout urls
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name="signup"),
    path('edit/', views.edit, name='edit'),
    path('404/', views.custom_404, name="404"),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
