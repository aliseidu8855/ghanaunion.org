from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MemberProfileUpdateForm

@login_required
def profile_view(request):
    """
    Display the user's profile page.
    """
    context = {
        'user_profile': request.user.profile
    }
    return render(request, 'pages/profile.html', context)


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = MemberProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = MemberProfileUpdateForm(instance=request.user.profile)

    context = {
        'form': form
    }
    return render(request, 'account/edit_profile.html', context)