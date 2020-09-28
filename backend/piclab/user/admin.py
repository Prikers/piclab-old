from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from piclab.user.models import Profile

User = get_user_model()


class UserAdmin(UserAdmin):
    list_display = (
        'email', 'username', 'id', 'date_joined', 'last_login', 'is_admin', 'is_staff',
        'profile_link',   
    )
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    def profile_link(self, obj):
        url = reverse('admin:user_profile_change', args=(obj.profile.id,))
        return format_html(f'<a href="{url}">Profile</a>')

    profile_link.short_description = 'profile'


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'user_link', 'current_project_link', 'projects_link',)
    readonly_fields = ('user',)

    def user_link(self, obj):
        url = reverse('admin:user_user_change', args=(obj.user.id,))
        return format_html(f'<a href="{url}">{obj.user.username}</a>')
    
    def current_project_link(self, obj):
        url = reverse('admin:api_project_change', args=(obj.current_project.id,))
        return format_html(f'<a href="{url}">{obj.current_project.name}</a>')
    
    def projects_link(self, obj):
        count = obj.user.projects.count()
        url = reverse('admin:api_project_changelist') + '?' + urlencode({'owner__id': f'{obj.id}'})
        return format_html(f'<a href="{url}">{count} Projects</a>')

    user_link.short_description = 'user'
    current_project_link.short_description = 'current project'
    projects_link.short_description = 'projects'
