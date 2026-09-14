from django import forms
from django.contrib.auth.models import User
from .models import Donor, BloodRequest, Feedback


class DonorSignUpForm(forms.Form):
    """Used on the home page to register a donor AND create their login account."""
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=100)
    blood_group = forms.ChoiceField(choices=Donor.BLOOD_GROUP_CHOICES)
    city = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username


class DonorEditForm(forms.ModelForm):
    """Used on the donor's own edit-profile page."""
    class Meta:
        model = Donor
        fields = ['name', 'blood_group', 'city', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'blood_group': forms.Select(),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['patient_name', 'blood_group', 'hospital_name', 'phone']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'message', 'rating']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience...'}),
        }
