from django import forms
from .models import Post
from .widgets import TrixEditorWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # Make sure to specify the model class
        fields = ['title', 'content']
        labels = {
            'title': 'Title',
            'content': 'Content',
            # Add other field labels as needed
        }

    content = forms.CharField(widget=TrixEditorWidget)

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')

        # Ensure the style attribute is preserved
        if content and '<img' in content:
            content = content.replace('<img', "<img style='max-width:100%; height:auto;'")
            cleaned_data['content'] = content

        return cleaned_data
