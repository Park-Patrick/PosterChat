from django.shortcuts import render
from .models import Post
from django.views.generic import (
	ListView

)
# Create your views here.

class PostListView(ListView):
	template_name = "poster/post_list.html"
	queryset = Post.objects.all()
	context_object_name = 'posts'

class PostListView2(ListView):
	template_name = "poster/post_list_2.html"
	queryset = Post.objects.all()
	context_object_name = 'posts'


class PostListView3(ListView):
	template_name = "poster/post_list_3.html"
	queryset = Post.objects.all()
	context_object_name = 'posts'