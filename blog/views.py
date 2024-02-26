# blog/views.py
from django.shortcuts import render, get_object_or_404

from .models import Post
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm
from .templatetags.safe_filters import sanitize_html
from .mixins import HtmlSanitizedCharField


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
        # Sanitize HTML content
        context['object'].content = sanitize_html(context['object'].content)

        return context


class PostCreateView(LoginRequiredMixin,
                     HtmlSanitizedCharField,
                     CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_gists'] = Post.objects.order_by('-date_posted')[:3]
        return context


# class PostUpdateView(LoginRequiredMixin,
#                      UserPassesTestMixin,
#                      HtmlSanitizedCharField,
#                      UpdateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'blog/post_form.html'

#     def test_func(self):
#         post = self.get_object()
#         return self.request.user == post.author


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

    def get_initial(self):
        initial = super().get_initial()
        return initial.copy() if initial else {}  # Ensure initial is not None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = self.get_initial()
        return kwargs

    def form_valid(self, form):
        # Handle form validation and saving
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
