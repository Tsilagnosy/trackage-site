from django.contrib import admin

from .models import (
    Publication,
    VisitorAnalytics,
    ContactMessage
)


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
	
	
	
	
	
	
	
	
	
	
