from django.contrib import admin
from .models import MembershipTier, MemberProfile

@admin.register(MembershipTier)
class MembershipTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')