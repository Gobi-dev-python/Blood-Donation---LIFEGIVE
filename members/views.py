from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Donor, BloodRequest, Feedback
from .forms import DonorSignUpForm, DonorEditForm, BloodRequestForm, FeedbackForm


def home(request):
    """Home page: donor registration (creates login) + feedback list/form."""
    signup_form = DonorSignUpForm()
    feedback_form = FeedbackForm()

    if request.method == 'POST':
        # Two different forms can post to this page — check which one
        if 'register_submit' in request.POST:
            signup_form = DonorSignUpForm(request.POST)
            if signup_form.is_valid():
                data = signup_form.cleaned_data
                user = User.objects.create_user(
                    username=data['username'],
                    password=data['password']
                )
                Donor.objects.create(
                    user=user,
                    name=data['name'],
                    blood_group=data['blood_group'],
                    city=data['city'],
                    phone=data['phone'],
                )
                login(request, user)
                messages.success(request, "Registration successful! You're now logged in.")
                return redirect('home')

        elif 'feedback_submit' in request.POST:
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                fb = feedback_form.save(commit=False)
                # Auto-link feedback to the logged-in donor, if any
                if request.user.is_authenticated:
                    fb.donor = Donor.objects.filter(user=request.user).first()
                fb.save()
                messages.success(request, "Thank you for your feedback!")
                return redirect('home')

    feedback_list = Feedback.objects.all()[:10]  # most recent 10

    return render(request, 'index.html', {
        'signup_form': signup_form,
        'feedback_form': feedback_form,
        'feedback_list': feedback_list,
    })


def donor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('donor_profile')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


def donor_logout(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect('home')


@login_required(login_url='login')
def donor_profile(request):
    """Donor views and edits their own details here."""
    donor = get_object_or_404(Donor, user=request.user)

    if request.method == 'POST':
        form = DonorEditForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, "Your details have been updated.")
            return redirect('donor_profile')
    else:
        form = DonorEditForm(instance=donor)

    return render(request, 'donor_profile.html', {'form': form, 'donor': donor})


def request_view(request):
    form = BloodRequestForm()
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Blood request submitted. Donors will be notified.")
            return redirect('request')

    donors = Donor.objects.all()
    return render(request, 'request.html', {'form': form, 'donors': donors})
