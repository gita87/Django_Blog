# blog/views.py
from django.shortcuts import render, get_object_or_404

from .models import Post
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm
from .templatetags.safe_filters import sanitize_html


def about(request):
    latest_gists = Post.objects.order_by('-date_posted')[:3]
    context = {'title': "About Page", 'latest_gists': latest_gists}
    return render(request, 'blog/about.html', context)


class PostListView(LoginRequiredMixin,
                   ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_gists'] = Post.objects.order_by('-date_posted')[:3]

        return context


class PostDetailView(LoginRequiredMixin,
                     DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_gists'] = Post.objects.order_by('-date_posted')[:3]

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_gists'] = Post.objects.order_by('-date_posted')[:3]
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author before saving

        # Sanitize HTML content using the sanitize_html function
        form.instance.content = sanitize_html(form.cleaned_data['content'])

        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_object(self, queryset=None):
        # Get the Post object for the update view
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def form_valid(self, form):
        # Sanitize HTML content using the sanitize_html function
        form.instance.content = sanitize_html(form.cleaned_data['content'])

        # Handle form validation and saving
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
