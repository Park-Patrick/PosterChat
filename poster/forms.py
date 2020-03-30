from django import forms
from .models import Poster, Comment
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit, Layout, Field


# class PostForm(forms.ModelForm):
#     helper = FormHelper()
#     helper.form_method = "POST"
#     helper.add_input(Submit('Post', 'Post', css_class='btn-pri'))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
