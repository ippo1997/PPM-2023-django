from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Address


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1


class CustomUserAdmin(UserAdmin):
    inlines = [AddressInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)