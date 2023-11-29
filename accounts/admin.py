from django.contrib import admin

from accounts.models import UserRole, Role

admin.site.register((Role, UserRole))

