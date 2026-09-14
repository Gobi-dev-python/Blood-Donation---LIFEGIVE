from django.contrib import admin
from .models import Donor, BloodRequest, Feedback


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'city', 'phone', 'created_at')
    list_filter = ('blood_group', 'city')
    search_fields = ('name', 'phone', 'city')


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'blood_group', 'hospital_name', 'phone', 'created_at')
    list_filter = ('blood_group',)
    search_fields = ('patient_name', 'hospital_name')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'donor', 'created_at')
    list_filter = ('rating',)
    search_fields = ('name', 'message')
