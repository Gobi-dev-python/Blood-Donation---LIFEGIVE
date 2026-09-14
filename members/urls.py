from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('request/', views.request_view, name='request'),
    path('login/', views.donor_login, name='login'),
    path('logout/', views.donor_logout, name='logout'),
    path('profile/', views.donor_profile, name='donor_profile'),
]
