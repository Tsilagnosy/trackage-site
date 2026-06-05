from django import forms
from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path

from .models import (
    Album,
    AlbumPhoto,
    Publication,
    PublicationReaction,
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
            created_photos = []
            for uploaded_file in uploaded_files:
                created_photos.append(AlbumPhoto.objects.create(album=obj, image=uploaded_file))
            if created_photos:
                obj.cover_image = created_photos[0].image
                obj.save(update_fields=['cover_image'])


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
        'reaction_count',
        'rating_stars',
        'is_published'
    )

    search_fields = ('title',)
    list_filter = (
        'is_published',
        'created_at'
    )
    change_list_template = 'admin/portfolio/publication_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'statistics/',
                self.admin_site.admin_view(self.statistics_view),
                name='portfolio_publication_statistics',
            ),
        ]
        return custom_urls + urls

    def statistics_view(self, request):
        publications = Publication.objects.annotate(
            reaction_count=Count('reactions')
        ).order_by('-reaction_count')[:10]
        total_reactions = PublicationReaction.objects.count()
        total_publications = Publication.objects.count()
        rating_summary = {
            '4 étoiles': Publication.objects.annotate(reaction_count=Count('reactions')).filter(reaction_count__gt=50).count(),
            '3 étoiles': Publication.objects.annotate(reaction_count=Count('reactions')).filter(reaction_count__gte=30, reaction_count__lte=50).count(),
            '2 étoiles': Publication.objects.annotate(reaction_count=Count('reactions')).filter(reaction_count__lt=30).count(),
        }

        context = {
            **self.admin_site.each_context(request),
            'title': 'Statistiques des publications',
            'publications': publications,
            'total_reactions': total_reactions,
            'total_publications': total_publications,
            'rating_summary': rating_summary,
        }

        return TemplateResponse(request, 'admin/portfolio/publication_statistics.html', context)

    def reaction_count(self, obj):
        return obj.reaction_count

    def rating_stars(self, obj):
        return '★' * obj.rating_stars


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
	
	
	
	
	
	
	
	
	
	
