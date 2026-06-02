from django.db import models


class Publication(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='publications/') #blank=True, null=True

    created_at = models.DateTimeField(auto_now_add=True)

    views = models.PositiveIntegerField(default=0)

    is_published = models.BooleanField(default=True)

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


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)

    email = models.EmailField()

    message = models.TextField()

    sent_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.name	
	
	
	
	
	
	
	
	
	
	