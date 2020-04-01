from django.urls import path, include
from . import views

app_name = 'poster'

urlpatterns = [
    path(
        'conferences/',
        views.ConferenceIndexView.as_view(),
        name='conference_index'
    ),
    path(
        'conferences/<int:conf_k>/',
        views.conference_detail,
        name='conference_detail'
    ),
    path(
        'conferences/<int:conf_k>/posters/<int:poster_pk>/',
        views.poster_detail,
        name='poster_detail'
    ),
    path(
        'conferences/<int:conf_k>/posters/create/',
        views.poster_update,
        name='poster_create'
    ),
    path(
        'conferences/<int:conf_k>/posters/<int:poster_pk>/update',
        views.poster_update,
        name='poster_update'
    ),
]
