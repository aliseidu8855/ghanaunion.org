from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'location', 'created_by', 'registration_deadline')
    list_filter = ('date_time', 'location')
    search_fields = ('title', 'description', 'location')
    raw_id_fields = ('created_by', 'attendees')