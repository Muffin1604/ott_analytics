
from django.contrib import admin
from .models import User, Video, WatchSession

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name','email','registration_date')
    search_fields = ('name','email')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title','genre','duration')
    list_filter = ('genre',)

@admin.register(WatchSession)
class WatchSessionAdmin(admin.ModelAdmin):
    list_display = ('user','video','start_time','session_duration','device_type','is_rewatch')
    list_filter = ('device_type','is_rewatch')
