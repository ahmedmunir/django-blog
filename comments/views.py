from django.shortcuts import render, reverse

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView

from blogapp.models import Post
from comments.models import Comment

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment

    fields = ['text']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['post_id'])
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment

    fields = ['text']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()

        if comment.owner == self.request.user:
            return True
        return False

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        self.comment = self.get_object()

        if self.comment.owner == self.request.user or self.comment.post.author == self.request.user:
            return True
        return False

    def get_success_url(self):
        return reverse('post-detail', args=[self.get_object().post.id])