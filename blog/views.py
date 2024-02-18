from django.shortcuts import render
from .models import Post
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
    )
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def about(request):
    latest_gists = Post.objects.order_by('-date_posted')[:3]
    context = {'title': "About Page", 'latest_gists': latest_gists}
    return render(request, 'blog/about.html', context)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the latest gists
        context['latest_gists'] = Post.objects.order_by('-date_posted')[:3]  # Assuming Gist model has a 'date' field
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the latest gists
        context['latest_gists'] = Post.objects.order_by('-date_posted')[:3]  # Assuming Gist model has a 'date' field
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the latest gists
        context['latest_gists'] = Post.objects.order_by('-date_posted')[:3]  # Assuming Gist model has a 'date' field
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
