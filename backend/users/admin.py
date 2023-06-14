from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Follow


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    # list_editable = ('username', 'email', 'first_name', 'last_name')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')
    list_filter = ('author', 'user')
