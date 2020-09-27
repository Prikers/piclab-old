from django.contrib import admin
from .models import Photo, Project


@admin.register(Project)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'owner', 'date_created')
    search_fields = ('name',)
    readonly_fields = ('owner', 'date_created')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'owner', 'project', 'date')
    search_fields = ('name',)
    readonly_fields = ('owner', 'date', 'owner', 'project')
