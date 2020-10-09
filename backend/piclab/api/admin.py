from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import Photo, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'owner_link', 'date_created', 'count_photos')
    search_fields = ('name',)
    readonly_fields = ('owner', 'date_created')

    def owner_link(self, obj):
        url = reverse('admin:user_user_changelist') + '?' + urlencode({'id': f'{obj.owner.id}'})
        return format_html(f'<a href="{url}">{obj.owner.username}</a>')

    def count_photos(self, obj):
        count = obj.photos.count()
        url = reverse('admin:api_photo_changelist') + '?' + urlencode({'project__id': f'{obj.id}'})
        return format_html(f'<a href="{url}">{count} Photos</a>')

    owner_link.short_description = 'owner'
    count_photos.short_description = '#photos'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'owner_link', 'project_link',
                    'date_created', 'like', 'photo_link')
    search_fields = ('name',)
    readonly_fields = ('owner', 'date_created', 'project')

    def owner_link(self, obj):
        url = reverse('admin:user_user_changelist') + '?' + urlencode({'id': f'{obj.owner.id}'})
        return format_html(f'<a href="{url}">{obj.owner.username}</a>')

    def project_link(self, obj):
        url = reverse('admin:api_project_changelist') + '?' + urlencode({'id': f'{obj.project.id}'})
        return format_html(f'<a href="{url}">{obj.project.name}</a>')

    def photo_link(self, obj):
        return format_html(f'<a href="{obj.image.url}">link</a>')
    
    def like(self, obj):
        return format_html('♥' if obj.is_liked else '')

    owner_link.short_description = 'owner'
    project_link.short_description = 'project'
    photo_link.short_description = 'link'
    like.short_description = 'like'
