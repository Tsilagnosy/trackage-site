from django import forms
from django.contrib import admin

from .models import (
    Album,
    AlbumPhoto,
    Publication,
    Video,
    VisitorAnalytics,
    ContactMessage,
)


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        attrs = {'multiple': True, **(attrs or {})}
        super().__init__(attrs=attrs)


class MultiFileField(forms.FileField):
    widget = MultiFileInput
    required = False
    MAX_FILES = 10
    default_error_messages = {
        'max_files': 'Sélectionnez au maximum %(max_files)s images.',
    }

    def clean(self, data, initial=None):
        if not data:
            return []

        if isinstance(data, (list, tuple)):
            if len(data) > self.MAX_FILES:
                raise forms.ValidationError(
                    self.error_messages['max_files'],
                    params={'max_files': self.MAX_FILES},
                )

            cleaned_files = []
            errors = []
            for uploaded_file in data:
                try:
                    cleaned_files.append(super().clean(uploaded_file, initial))
                except forms.ValidationError as exc:
                    errors.extend(exc.error_list)
            if errors:
                raise forms.ValidationError(errors)
            return cleaned_files

        return [super().clean(data, initial)]


class AlbumAdminForm(forms.ModelForm):
    new_photos = MultiFileField(
        required=False,
        label='Ajouter des photos',
        help_text='Sélectionnez jusqu’à 10 images à la fois ; la première sera utilisée comme couverture.',
    )

    class Meta:
        model = Album
        fields = '__all__'


class AlbumPhotoInline(admin.TabularInline):
    model = AlbumPhoto
    extra = 0
    fields = ('image', 'caption')
    readonly_fields = ()


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    form = AlbumAdminForm
    list_display = ('title', 'created_at', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AlbumPhotoInline]
    search_fields = ('title', 'description')
    list_filter = ('is_published', 'created_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        uploaded_files = request.FILES.getlist('new_photos')
        if uploaded_files:
            obj.cover_image = uploaded_files[0]
            obj.save(update_fields=['cover_image'])
            for uploaded_file in uploaded_files:
                AlbumPhoto.objects.create(album=obj, image=uploaded_file)


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
	
	
	
	
	
	
	
	
	
	
