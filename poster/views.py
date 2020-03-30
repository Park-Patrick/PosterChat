from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Poster, Conference
from .forms import CommentForm


class IndexView(generic.ListView):
    template_name = "poster/conference_index.html"
    queryset = Conference.objects.all()
    context_object_name = 'latest_conferences'

    def get_queryset(self):
        return Conference.objects.order_by('-created_date')[:100]


class DetailView(generic.DetailView):
    model = Conference
    template_name = "poster/conference_detail.html"
    context_object_name = "conference"


def conference_detail(request, pk):
    template_name = "poster/conference_detail.html"
    conference = get_object_or_404(Conference, pk=pk)
    posters = conference.poster_set.all()

    return render(request, template_name, {
        "conference": conference,
        "posters": posters,
    })


def poster_detail(request, pk):
    template_name = 'poster/poster_detail.html'
    poster = get_object_or_404(Poster, pk=pk)
    comments = poster.comment_set.filter(active=True)

    new_comment = None
    if request.method != "POST":
        comment_form = CommentForm()
    else:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object

            new_comment = comment_form.save(commit=False)
            new_comment.poster = poster
            new_comment.user = request.user
            new_comment.save()

    return render(request, template_name, {
        "poster": poster,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
    })
