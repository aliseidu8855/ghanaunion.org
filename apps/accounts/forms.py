from allauth.account.forms import SignupForm
from django import forms
from apps.membership.models import MemberProfile

class CustomSignupForm(SignupForm):
    """
    Custom signup form to create a MemberProfile upon registration.
    """
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)

    def save(self, request):
        # Call the parent save method to create the user
        user = super(CustomSignupForm, self).save(request)

        # Save first_name and last_name to the user model
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # Create a MemberProfile for the new user
        MemberProfile.objects.create(user=user)

        return user


class MemberProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['profile_photo', 'phone', 'location', 'profession', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }



