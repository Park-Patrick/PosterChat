from django.urls import path, include
from .views import (
	PostListView
)

app_name = 'poster'

urlpatterns = [
#local : http://127.0.0.1:8000/
	path('', PostListView.as_view(), name='post_list')
]