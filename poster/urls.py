from django.urls import path, include
from . import views

app_name = 'poster'

urlpatterns = [
    path('', views.IndexView.as_view(), name='conference_index'),
    path('<int:pk>/', views.conference_detail, name='conference_detail'),
    path('poster/<int:pk>/', views.poster_detail, name='poster_detail'),
]
