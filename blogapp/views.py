from django.contrib import messages

from django.shortcuts import render, get_object_or_404

from blogapp.models import Post
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'blogapp/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    #paginator
    #that will define how many Post elements will be displayed per page (here we defined it to be 2)
    #now inside URL we can type /?page=2 will redirect to page number 2 and can be 3 and so on.
    paginate_by = 4

    #paginator will pass those variables to front end, which will be find at home.html

class UserPostListView(ListView):
    model = Post
    template_name = 'blogapp/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):

        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
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

def about(request):
    return render(request, 'blogapp/about.html')