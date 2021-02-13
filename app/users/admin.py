from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#substituting-a-custom-user-model
admin.site.register(User, UserAdmin)
