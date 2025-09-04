
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', include('apps.dashboard.urls')),
    path('events/', include('apps.events.urls')),
    path("membership/", include("apps.membership.urls")),
    path("news/", include("apps.news.urls")),

    # Add allauth and our accounts app URLs
    path('accounts/', include('allauth.urls')),
    path('', include('apps.accounts.urls')), # For our custom profile URL
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)