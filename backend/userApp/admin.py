from django.contrib import admin
from .models import MyUser

class MyUserAdmin(admin.ModelAdmin):
    model = MyUser
    list_display = ['email', 'username', 'is_active', 'registration_date']
    list_filter = ['is_active']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'registration_date', 'is_active', 'id_frame', 'activation_token')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'is_active', 'id_frame', 'activation_token')}),
    )

admin.site.register(MyUser, MyUserAdmin)