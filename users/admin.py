from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, UserAddress, UserInfo

admin.site.register(User)
admin.site.register(UserAddress)
admin.site.register(UserInfo)
# admin.site.unregister(Group)
