from django.contrib import admin
from .models import UserProfile, UserSet

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserSet)
