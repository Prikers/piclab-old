from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from piclab.user.models import Profile

User = get_user_model()


class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'id', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_field = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'current_project')
    readonly_fields = ('user',)
