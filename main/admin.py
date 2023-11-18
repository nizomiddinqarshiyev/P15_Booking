from django.contrib import admin
from accounts.models import Role, UserRole
from .models import Stay, Category, Image

admin.site.register((Stay, Category, Role, UserRole, Image))
