from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Account, Address

# https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#extending-the-existing-user-model
class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (AccountInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Address)