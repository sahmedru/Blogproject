from django import forms
from .models import posts, comments

class PostForm(forms.ModelForm):
    class Meta:
        model = posts
        fields = ['title', 'content', 'category', 'tag']  # Add 'category' and 'tag' fields to the form

class CommentForm(forms.ModelForm):
    class Meta:
        model = comments
        fields = ['content']