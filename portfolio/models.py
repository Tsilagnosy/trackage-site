from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Publication(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='publications/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def reaction_count(self):
        return self.reactions.count()

    @property
    def rating_stars(self):
        count = self.reaction_count
        if count > 50:
            return 4
        if 30 <= count <= 50:
            return 3
        return 2


class Album(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='albums/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='Album publié')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('album_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class AlbumPhoto(models.Model):
    album = models.ForeignKey(Album, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='album_photos/')
    caption = models.CharField(max_length=220, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.caption or f"Photo de {self.album.title}"


class Video(models.Model):
    album = models.ForeignKey(Album, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='Vidéo publiée')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class VisitorAnalytics(models.Model):
    ip_address = models.GenericIPAddressField()
    path_visited = models.CharField(max_length=255)

    browser = models.CharField(max_length=255, blank=True)
    device = models.CharField(max_length=255, blank=True)

    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path_visited}"


class PublicationReaction(models.Model):
    publication = models.ForeignKey(
        'Publication',
        related_name='reactions',
        on_delete=models.CASCADE
    )
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('wow', 'Wow'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
    ]

    kind = models.CharField(max_length=10, choices=REACTION_CHOICES, default='like')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    visitor_id = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reaction ({self.kind}) pour {self.publication.title} - {self.created_at:%Y-%m-%d %H:%M}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.name	
	
	
	
	
	
	
	
	
	
	