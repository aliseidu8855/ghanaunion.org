from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from apps.membership.models import MemberProfile

class MemberProfileInline(admin.StackedInline):
    model = MemberProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = (MemberProfileInline, )
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'get_membership_tier', # Custom method
        'get_is_approved'      # Custom method
    )
    list_select_related = ('profile', 'profile__membership_tier')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'profile__is_approved', 'profile__membership_tier')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'profile__profession')
    actions = ['approve_members'] # Add custom action

    # Custom methods to display profile data in the user list
    @admin.display(description='Membership Tier', ordering='profile__membership_tier')
    def get_membership_tier(self, obj):
        if hasattr(obj, 'profile') and obj.profile.membership_tier:
            return obj.profile.membership_tier.name
        return 'N/A'

    @admin.display(description='Approved', ordering='profile__is_approved', boolean=True)
    def get_is_approved(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.is_approved
        return False

    # Custom admin action
    @admin.action(description='Approve selected members')
    def approve_members(self, request, queryset):
        # We update the related MemberProfile, not the user itself
        profiles_updated = 0
        for user in queryset:
            if hasattr(user, 'profile'):
                user.profile.is_approved = True
                user.profile.save()
                profiles_updated += 1
        
        self.message_user(request, f'{profiles_updated} members were successfully approved.', messages.SUCCESS)
