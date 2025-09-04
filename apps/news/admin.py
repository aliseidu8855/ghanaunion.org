from django.contrib import admin
from .models import NewsPost, Tag

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_featured')
    list_filter = ('is_featured', 'published_date', 'tags')
    search_fields = ('title', 'content')
    prepopulated_fields = {} # If you add a slug field, use {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)