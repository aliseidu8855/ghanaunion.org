from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth
from apps.accounts.models import CustomUser
from apps.membership.models import MembershipTier
import json

@staff_member_required
def analytics_dashboard_view(request):
    """
    Custom admin view for displaying member analytics.
    """

    member_growth = (
        CustomUser.objects
        .annotate(month=TruncMonth('date_joined'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    growth_labels = [g['month'].strftime('%b %Y') for g in member_growth]
    growth_data = [g['count'] for g in member_growth]


    tier_distribution = (
        MembershipTier.objects
        .annotate(member_count=Count('memberprofile'))
        .values('name', 'member_count')
    )

    tier_labels = [t['name'] for t in tier_distribution]
    tier_data = [t['member_count'] for t in tier_distribution]


    geo_distribution = (
        CustomUser.objects
        .exclude(profile__location__exact='')
        .values('profile__location')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    geo_labels = [g['profile__location'] for g in geo_distribution]
    geo_data = [g['count'] for g in geo_distribution]

    context = {
        'title': 'Analytics Dashboard',
        'total_members': CustomUser.objects.count(),
        'pending_approval': CustomUser.objects.filter(profile__is_approved=False).count(),
        'growth_labels': json.dumps(growth_labels),
        'growth_data': json.dumps(growth_data),
        'tier_labels': json.dumps(tier_labels),
        'tier_data': json.dumps(tier_data),
        'geo_labels': json.dumps(geo_labels),
        'geo_data': json.dumps(geo_data),
    }
    return render(request, 'dashboard/analytics.html', context)

