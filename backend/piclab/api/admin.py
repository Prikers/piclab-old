from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import Photo, Project, Hash


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
                    'datetime_uploaded', 'datetime_photo',
                    'like', 'photo_link', 'hash_link')
    search_fields = ('name',)
    readonly_fields = ('owner', 'datetime_uploaded', 'project')

    def owner_link(self, obj):
        url = reverse('admin:user_user_changelist') + '?' + urlencode({'id': f'{obj.owner.id}'})
        return format_html(f'<a href="{url}">{obj.owner.username}</a>')

    def project_link(self, obj):
        url = reverse('admin:api_project_changelist') + '?' + urlencode({'id': f'{obj.project.id}'})
        return format_html(f'<a href="{url}">{obj.project.name}</a>')

    def hash_link(self, obj):
        url = reverse('admin:api_hash_changelist') + '?' + urlencode({'id': f'{obj.hash.id}'})
        return format_html(f'<a href="{url}">hash</a>')

    def photo_link(self, obj):
        return format_html(f'<a href="{obj.image.url}">link</a>')
    
    def like(self, obj):
        return format_html('♥' if obj.is_liked else '')

    def size(self, obj):
        return format_html(f'({obj.width}, {obj.height})')

    owner_link.short_description = 'owner'
    project_link.short_description = 'project'
    photo_link.short_description = 'link'
    hash_link.short_description = 'hash'
    like.short_description = 'like'


@admin.register(Hash)
class HashAdmin(admin.ModelAdmin):
    list_display = ('id', 'hash_short', 'photo_link', 'is_duplicated', 'duplicate_id', 'status', 'date_status')
    search_fields = ('photo',)
    readonly_fields = ('photo', 'hash')

    def photo_link(self, obj):
        url = reverse('admin:api_photo_changelist') + '?' + urlencode({'id': f'{obj.photo.id}'})
        return format_html(f'<a href="{url}">{obj.photo.name}</a>')
    
    def hash_short(self, obj):
        return obj.hash[:20] + '...'

    photo_link.short_description = 'photo'
