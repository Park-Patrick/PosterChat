from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect

from .forms import UpdateUserForm


def profile(request, username):
    template_name = "core/profile.html"
    profile = get_object_or_404(get_user_model(), username=username)
    return render(request, template_name, {"profile": profile})


def home(request):
    template_name = "core/home.html"
    return render(request, template_name, {})


def update_user(request, username):
    if request.method == "POST":
        user = UpdateUserForm(request.POST)
        if user.is_valid():
            return HttpResponseRedirect("/")

    else:
        profile = get_object_or_404(get_user_model(), username=username)
        context = {"profile": profile}

        if request.user.is_authenticated:
            form = UpdateUserForm(instance=request.user)
            context["form"] = form

        return render(request, "core/profile_edit.html", context)
