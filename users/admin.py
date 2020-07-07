from django.contrib import admin
from .models import User

# Register your models here.
class UserAmin(admin.ModelAdmin):
    list_display = ['firstName', 'lastName', 'email', 'createdAt', 'updatedAt']
    list_filter = ['createdAt', 'email']
    search_fields = ['email']

admin.site.register(User, UserAmin)
