from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import decorators
from django.views import generic
from .models import Poster, Conference
from .forms import CommentForm, PosterForm
from PIL import Image
import datetime


class ConferenceIndexView(generic.ListView):
    template_name = "poster/conference_index.html"
    queryset = Conference.objects.all()
    context_object_name = 'latest_conferences'

    def get_queryset(self):
        return Conference.objects.order_by('-created_date')[:100]


@decorators.login_required
def conference_detail(request, conf_k):
    template_name = "poster/conference_detail.html"
    conference = get_object_or_404(Conference, pk=conf_k)

    posters = conference.poster_set.all()

    organizers = conference.organizers.all()
    attendees = conference.attendees.all()
    guests = conference.attendees.all()

    is_organizer = request.user.is_authenticated and request.user in organizers

    return render(request, template_name, {
        "conference": conference,
        "posters": posters,
        "organizers": organizers,
        "attendees": attendees,
        "guests": guests,
        "is_organizer": is_organizer,
    })


@decorators.login_required
def poster_create(request, conf_k):
    template_name = "poster/poster_create.html"
    context = {}

    if request.method == "POST":
        poster_form = PosterForm(data=request.POST, files=request.FILES)
        conference = get_object_or_404(Conference, pk=conf_k)
        if poster_form.is_valid():
            new_poster = poster_form.save(commit=False)
            # new_poster.authors.add(request.user)
            new_poster.created_date = datetime.datetime.now()
            new_poster.conference = conference

            destination = new_poster.image.path

            new_poster.save()
        return HttpResponseRedirect("/")

    else:
        form = PosterForm()
        context["form"] = form
        return render(request, template_name, context)


@decorators.login_required
def poster_update(request, conf_k, poster_pk=None):
    template_name = "poster/poster_create.html"
    context = {}

    if request.method == "POST":
        poster_form = PosterForm(data=request.POST, files=request.FILES)
        conference = get_object_or_404(Conference, pk=conf_k)
        if poster_form.is_valid():
            new_poster = poster_form.save(commit=False)
            # new_poster.authors.add(request.user)
            new_poster.created_date = datetime.datetime.now()
            new_poster.conference = conference

            new_poster.save()
        return HttpResponseRedirect("/")

    elif poster_pk:
        poster = get_object_or_404(Poster, pk=poster_pk)
        context["poster"] = poster
        form = PosterForm(instance=poster)
    else:
        form = PosterForm()

    context["form"] = form
    return render(request, template_name, context)


@decorators.login_required
def poster_detail(request, conf_k, poster_pk):
    template_name = 'poster/poster_detail.html'
    poster = get_object_or_404(Poster, pk=poster_pk)
    conference = get_object_or_404(Conference, pk=conf_k)

    comments = poster.comment_set.filter(active=True)

    organizers = conference.organizers.all()
    attendees = conference.attendees.all()
    guests = conference.attendees.all()
    authors = poster.authors.all()

    is_editable = request.user in organizers or request.user in authors
    can_comment = request.user in organizers or request.user in attendees or request.users in authors

    new_comment = None
    if request.method != "POST":
        comment_form = CommentForm()
    else:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object

            new_comment = comment_form.save(commit=False)
            new_comment.poster = poster
            new_comment.author = request.user
            new_comment.save()

    return render(request, template_name, {
        "poster": poster,
        "conference": conference,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
        "is_editable": is_editable,
        "can_comment": can_comment,
    })
