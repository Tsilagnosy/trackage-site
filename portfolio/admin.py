from django.contrib import admin

from .models import (
    Album,
    Publication,
    Video,
    VisitorAnalytics,
    ContactMessage,
)


class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    fields = ('title', 'video_file', 'video_url', 'is_published')


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [VideoInline]
    search_fields = ('title', 'description')
    list_filter = ('is_published', 'created_at')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'description', 'album__title')


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created_at',
        'views',
        'is_published'
    )

    search_fields = ('title',)
    list_filter = (
        'is_published',
        'created_at'
    )


@admin.register(VisitorAnalytics)
class VisitorAnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        'ip_address',
        'path_visited',
        'browser',
        'device',
        'visited_at'
    )

    search_fields = (
        'ip_address',
        'browser'
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'sent_at',
        'is_read'
    )

    list_filter = (
        'is_read',
    )	
	
	
	
	
	
	
	
	
	
	
