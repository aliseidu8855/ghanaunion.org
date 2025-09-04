from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.membership.models import MembershipTier
from paystackapi.paystack import Paystack
# Initialize Paystack
paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)

@login_required
def membership_plans_view(request):
    """Displays the membership pricing plans."""
    membership_tiers = MembershipTier.objects.all()
    context = {
        'membership_tiers': membership_tiers,
    }
    return render(request, 'pages/membership_plans.html', context)

@login_required
def initiate_payment_view(request, tier_id):
    """Initiates a payment with Paystack."""
    tier = get_object_or_404(MembershipTier, id=tier_id)
    amount_in_pesewas = int(tier.price * 100)

    # Create a unique reference for the transaction
    # This is important for tracking
    reference = f"GU-{request.user.id}-{tier.id}-{int(timezone.now().timestamp())}"

    try:
        response = paystack.transaction.initialize(
            reference=reference,
            amount=amount_in_pesewas,
            email=request.user.email,
            currency='GHS',
            callback_url=request.build_absolute_uri(
                reverse('membership:payment_callback')
            ),
            metadata={
                'user_id': request.user.id,
                'tier_id': tier.id,
                'custom_fields': [
                    {'display_name': "Member", 'variable_name': "member_name", 'value': request.user.get_full_name()},
                    {'display_name': "Membership Tier", 'variable_name': "membership_tier", 'value': tier.name},
                ]
            }
        )

        if response['status']:
            payment_url = response['data']['authorization_url']
            return redirect(payment_url)
        else:
            messages.error(request, "Could not initiate payment. Please try again.")
            return redirect('membership:plans')

    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('membership:plans')

@login_required
def payment_callback_view(request):
    """Handles the callback from Paystack after payment."""
    reference = request.GET.get('reference')

    if not reference:
        messages.error(request, "No payment reference found.")
        return redirect('membership:plans')

    try:
        response = paystack.transaction.verify(reference=reference)

        if response['data']['status'] == 'success':
            # Payment was successful
            metadata = response['data']['metadata']
            user_id = metadata.get('user_id')
            tier_id = metadata.get('tier_id')

            # Verify that the user in the session is the one who paid
            if str(request.user.id) == str(user_id):
                tier = get_object_or_404(MembershipTier, id=tier_id)
                request.user.profile.membership_tier = tier
                request.user.profile.save()
                messages.success(request, f"Payment successful! You are now a {tier.name} member.")
                return redirect('profile')
            else:
                messages.error(request, "Payment verification failed (user mismatch). Please contact support.")
                return redirect('membership:plans')
        else:
            # Payment was not successful
            messages.error(request, f"Payment failed. Status: {response['data']['status']}")
            return redirect('membership:plans')

    except Exception as e:
        messages.error(request, f"An error occurred during verification: {e}")
        return redirect('membership:plans')
