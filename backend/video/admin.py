from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'slug', 'author', 'uploaded_at')
    prepopulated_fields = {'slug': ('title',)}

