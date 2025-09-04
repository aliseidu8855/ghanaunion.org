from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from apps.news.models import NewsPost, Tag
from django.utils import timezone

class NewsListView(ListView):
    model = NewsPost
    template_name = 'pages/news_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = NewsPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        
        # Tag filtering functionality
        tag_name = self.kwargs.get('tag_name')
        if tag_name:
            queryset = queryset.filter(tags__name__iexact=tag_name)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['current_tag'] = self.kwargs.get('tag_name')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class NewsDetailView(DetailView):
    model = NewsPost
    template_name = 'pages/news_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = NewsPost.objects.filter(published_date__lte=timezone.now()).exclude(pk=self.object.pk).order_by('-published_date')[:3]
        context['tags'] = Tag.objects.all()
        return context