from django import forms
from .models import Post
from .widgets import TrixEditorWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        labels = {
            'title': 'Title',
            'content': 'Content',
        }
        widgets = {'content': TrixEditorWidget}
