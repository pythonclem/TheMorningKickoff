from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'username', 'email', 'created')
    list_filter = ('created', 'teams')
    search_fields = ('user__username', 'name', 'username', 'email')
    ordering = ('id',)

admin.site.register(Profile, ProfileAdmin)