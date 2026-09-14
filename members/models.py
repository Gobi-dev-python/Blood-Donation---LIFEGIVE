from django.db import models
from django.contrib.auth.models import User


class Donor(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    # Links each donor record to a login account.
    # null=True lets old donor rows (created before login existed) keep working.
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.blood_group})"


class BloodRequest(models.Model):
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5)
    hospital_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.blood_group}"


class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    name = models.CharField(max_length=100)
    # Optional link — filled in automatically if the person is logged in
    donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(max_length=500)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback from {self.name} ({self.rating}★)"
