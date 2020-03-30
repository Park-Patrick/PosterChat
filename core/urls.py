from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('profile/<slug:username>/edit/',
         views.update_user, name='profile_edit'),
    path('', views.home, name='home'),
]
