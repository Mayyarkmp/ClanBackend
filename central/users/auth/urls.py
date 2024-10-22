from django.urls import path
from central.users.auth import views

app_name = 'clan'

urlpatterns = [
    # path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    # path('verify/phone/', views.PhoneVerify.as_view(), name='verify_phone'),
    # path('verify/email/', views.EmailVerify.as_view(), name='verify_email'),
    # path('password-reset/request/', views.PasswordResetRequest.as_view(), name='password_reset_request'),
    # path('password-reset/confirm/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    # path('resend-otp/', views.ResendOTP.as_view(), name='resend_otp'),
    # path('card-id/', views.CardID.as_view(), name='card_id'),
    # path('google/', views.GoogleAuth.as_view(), name='google_login'),
    # path('apple/', views.AppleAuth.as_view(), name='apple_login'),
    # path('phone/', views.PhoneAuth.as_view(), name='phone_login'),
    path('status/', views.ClanUserStatus.as_view(), name='clan_status'),

]