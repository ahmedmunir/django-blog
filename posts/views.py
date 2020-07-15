from django.shortcuts import render, get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

from posts.models import Post
from users.models import UserCustom
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

class PostListView(ListView):
    """
        List all posts 
    """
    
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class UserPostListView(ListView):
    """
        List all posts created by specific User
    """
    
    model = Post
    template_name = 'posts/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(UserCustom, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    """
        All details about specific Post
    """
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    """
        Create new Post
    """

    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):

        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
        Update Post
    """
    model = Post
    success_message = "You updated post Successfully"
    fields = ['title', 'content']

    def form_valid(self, form):

        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        #get post object that created
        post = self.get_object()

        if post.author == self.request.user:
            return True
        return False        

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
        Delete Post
    """
    model = Post
    success_url = '/'

    def test_func(self):
        #get post object that created
        post = self.get_object()

        if post.author == self.request.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.warning(self.request, "You deleted post successfully")
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

