from django.urls import path, include

app_name = 'central'

urlpatterns = [
    path('users/', include('central.users.urls', namespace='users')),
]