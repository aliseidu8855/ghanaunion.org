from django.db import models
from apps.accounts.models import CustomUser


class MembershipTier(models.Model):
    """Defines the different membership levels."""
    TIER_CHOICES = [
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
        ('Lifetime', 'Lifetime'),
    ]
    name = models.CharField(max_length=50, choices=TIER_CHOICES, unique=True)
    description = models.TextField(help_text="Detailed benefits of this tier.")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in GHS")

    def __str__(self):
        return self.name

class MemberProfile(models.Model):
    """Stores additional information for a user who is a member."""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    membership_tier = models.ForeignKey(
        MembershipTier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        default='profile_photos/default.png',
        blank=True
    )
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(
        default=False,
        help_text="Designates whether the member's registration is approved by an admin."
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"