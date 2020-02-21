from django.urls import path, include
from .views import (
	PostListView,
	PostListView2,
	PostListView3,
)

app_name = 'poster'

urlpatterns = [
#local : http://127.0.0.1:8000/
	path('', PostListView.as_view(), name='post_list'),
	path('1/', PostListView2.as_view(), name='post_list_2'),
	path('2/', PostListView3.as_view(), name='post_list_3')
]