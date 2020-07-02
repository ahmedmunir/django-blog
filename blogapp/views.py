from django.contrib import messages

from django.shortcuts import render

from blogapp.models import Post

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