from django import forms
from .models import Post
from .widgets import TrixEditorWidget
import sys


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        labels = {
            'title': 'Title',
            'content': 'Content',
        }
        widgets = {'content': TrixEditorWidget}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set initial content from instance if available
        if self.instance and 'content' not in self.initial:
            print("Setting initial content:", self.instance.content, file=sys.stdout)
            self.initial['content'] = self.instance.content
            print("Updated initial content:", self.initial['content'], file=sys.stdout)


    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')

        # Ensure the style attribute is preserved
        if content and '<img' in content:
            content = content.replace('<img', "<img style='max-width:100%; height:auto;'")
            print("content : ", content)
            cleaned_data['content'] = content

        return cleaned_data
