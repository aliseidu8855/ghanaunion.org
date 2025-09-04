from django.db import models
from django.conf import settings

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='news_images/', help_text="Image should be 1200x800 pixels.")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    published_date = models.DateTimeField()
    is_featured = models.BooleanField(default=False, help_text="Featured posts may appear on the homepage.")
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title