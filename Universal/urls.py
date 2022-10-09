from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='registration'),
    path('verify-user/<slug:uEid>/<slug:token>/', views.UserOtpVerificationView.as_view(), name='VerifyUserRegisterOtp'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('changepassword/', views.ChangeUserPasswordView.as_view(), name='changepassword'),
    path('send-reset-password-otp/', views.SendPasswordResetEmailView.as_view(), name='resetPassOtp'),
    path('reset-password/<slug:uEid>/<slug:token>/', views.UserPasswordResetView.as_view(), name='VerifyPasswordResetOtp'),
]