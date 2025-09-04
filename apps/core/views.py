
from django.shortcuts import render
from django.utils import timezone
from apps.events.models import Event
from apps.news.models import NewsPost
from apps.accounts.models import CustomUser

def home(request):
    # Fetch the next 3 upcoming events
    upcoming_events = Event.objects.filter(
        date_time__gte=timezone.now()
    ).order_by('date_time')[:3]

    # Fetch latest 3 news posts
    latest_news = NewsPost.objects.order_by('-published_date')[:3]

    # Get statistics
    member_count = CustomUser.objects.filter(profile__is_approved=True).count()

    context = {
        'upcoming_events': upcoming_events, # Changed from 'next_event'
        'latest_news': latest_news,
        'member_count': member_count,
    }
    return render(request, 'pages/home.html', context)