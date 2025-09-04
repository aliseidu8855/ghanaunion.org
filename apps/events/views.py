
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.events.models import Event

class EventListView(ListView):
    model = Event
    template_name = 'pages/event_list.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Event.objects.filter(title__icontains=query).order_by('date_time')
        return Event.objects.all().order_by('date_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        # We get the full queryset from the parent method
        all_events = self.get_queryset()
        context['upcoming_events'] = all_events.filter(date_time__gte=now)
        context['past_events'] = all_events.filter(date_time__lt=now).order_by('-date_time')
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'pages/event_detail.html'
    context_object_name = 'event' # Explicitly name the context object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        
        # **CRITICAL FIX:** Add 'now' to the context
        context['now'] = timezone.now()

        if self.request.user.is_authenticated:
            context['is_attending'] = event.attendees.filter(id=self.request.user.id).exists()
        else:
            context['is_attending'] = False
        return context

@login_required
def event_rsvp_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Check if the event is in the past
    if event.date_time < timezone.now():
        messages.error(request, "You cannot RSVP for an event that has already passed.")
        return redirect('events:detail', pk=event.pk)

    if request.method == 'POST':
        if event.attendees.filter(id=request.user.id).exists():
            event.attendees.remove(request.user)
            messages.success(request, "You have successfully cancelled your RSVP.")
        else:
            event.attendees.add(request.user)
            messages.success(request, "Thank you for your RSVP! We look forward to seeing you.")
    
    return redirect('events:detail', pk=event.pk)