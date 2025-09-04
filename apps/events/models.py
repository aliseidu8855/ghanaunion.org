from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    featured_image = models.ImageField(upload_to='event_images/', help_text="Image should be 1200x800 pixels.")
    max_attendees = models.PositiveIntegerField(null=True, blank=True, help_text="Leave blank for unlimited.")
    registration_deadline = models.DateTimeField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_events'
    )
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='attended_events',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_time']

    def __str__(self):
        return self.title