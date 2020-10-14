from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    List_display = ('user')

admin.site.register(Profile, ProfileAdmin)