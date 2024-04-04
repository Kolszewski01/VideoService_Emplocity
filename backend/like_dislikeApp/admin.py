from django.contrib import admin
from .models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'like')
    list_filter = ('like',)
    search_fields = ('user__username', 'video__title')



