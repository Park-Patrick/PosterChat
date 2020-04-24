from django import forms
from .models import Poster, Comment


class PosterForm(forms.ModelForm):
    class Meta:
        model = Poster
        fields = ('title', 'subtitle', 'description', 'image',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
