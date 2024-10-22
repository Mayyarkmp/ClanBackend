from django.urls import path
from customers.auth import views

app_name = 'auth'

urlpatterns = [
    path('phone/', views.PhoneAuth.as_view(), name='phone'),
    path('phone/verify/', views.PhoneVerify.as_view(), name='phone-verify'),
    path('phone/resend/', views.ResendOTP.as_view(), name='phone-resend'),
    path('google/', views.GoogleAuth.as_view(), name='google'),
    path('apple/', views.AppleAuth.as_view(), name='apple'),
]