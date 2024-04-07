from django.contrib import admin
from .models import Comment, Video

# Rejestracja modelu Video pozostaje bez zmian
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'slug', 'author', 'uploaded_at')
    prepopulated_fields = {'slug': ('title',)}

# Rejestracja modelu Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content_short', 'created_at', 'video', 'parent')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username')

    def content_short(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_short.short_description = 'Treść'
