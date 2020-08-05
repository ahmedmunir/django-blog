from django.shortcuts import render, get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
    View
)

from posts.models import Post, Category
from users.models import NewUser
from marketing.models import SignUp
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.contrib import messages
from django.shortcuts import redirect

from django.db.models import Count, Q
# Create your views here.

class HomeView(ListView):
    """
        Home Page, has latest 3 posts + 3 Featured Posts
    """
    
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.filter(featured=True)[0:3]
        return queryset

    def get_context_data(self, **kwargs):

        # call base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # add a queryset of last 3 added posts
        context['latest_posts'] = Post.objects.filter(featured=False).order_by('-date_posted')[0:3]
        return context

    # Accept post requests here, to register Email for subscription for newsletter
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        new_signup = SignUp()
        new_signup.email = email
        new_signup.save()

        messages.success(request, 'You successfully registered for newsletter for our website')
        return redirect('blog-home')

class PostsListView(ListView):
    """
        Display all posts
    """
    model = Post
    template_name='posts/blog.html'
    context_object_name = "rest_posts"
    paginate_by = 4

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-view_count')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.all().order_by('-date_posted')[0:3]
        context['categories'] = Post \
                        .objects \
                        .values('categories__title') \
                        .annotate(Count('categories__title'))
        return context

class UserPostListView(ListView):
    """
        List all posts created by specific User
    """
    
    model = Post
    template_name = 'posts/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(NewUser, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aboutuser'] = NewUser.objects.filter(username=self.kwargs.get('username')).first()
        print(context['aboutuser'].profile.image.url)
        return context


class PostDetailView(DetailView):
    """
        All details about specific Post
    """
    model = Post

    def get_object(self):
        queryset = Post.objects.get(pk=self.kwargs.get('pk'))
        queryset.view_count += 1
        queryset.save()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.all().order_by('-date_posted')[0:3]
        context['categories'] = Post \
                                .objects \
                                .values('categories__title') \
                                .annotate(Count('categories__title'))
        try:
            context['next_post'] = Post.objects.get(id=self.kwargs.get('pk') + 1)
        except:
            context['next_post'] = None
        try:
            context['previous_post'] = Post.objects.get(id=self.kwargs.get('pk') - 1)
        except:
            context['previous_post'] = None
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """
        Create new Post
    """

    model = Post
    fields = ['title', 'overview', 'content', 'thumbnail', 'categories']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = 'Create'
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
        Update Post
    """
    model = Post
    success_message = "You updated post Successfully"
    fields = ['title', 'overview', 'content', 'thumbnail', 'categories']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        #get post object that created
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = 'Update'
        return context        

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


class SearchView(View):
    """
        search using title or overview
    """

    def get(self, request):
        query = request.GET.get('q')
        tag   = request.GET.get('tag')

        #get values using title or overview
        if query and tag:
            search_results = Post.objects.filter(
                Q(categories__title = tag),
                Q(title__contains=query) |
                Q(title__contains=query.upper())|
                Q(title__contains=query.lower())| 
                Q(overview__contains=query)|
                Q(overview__contains=query.upper())|
                Q(overview__contains=query.lower()) 
            )
            
        elif query:
            search_results = Post.objects.filter(
                Q(title__contains=query) |
                Q(title__contains=query.upper())|
                Q(title__contains=query.lower())| 
                Q(overview__contains=query)|
                Q(overview__contains=query.upper())|
                Q(overview__contains=query.lower()) 
            )

        elif tag:
            search_results = Post.objects.filter(categories__title = tag)

        else:
            return render(request, "posts/search_results.html", {"error": "Can't find any result"})
        
        # Get distict values from categories to display unique values of them
        categories = Category.objects.filter(post__in=search_results).distinct()

        # make pagination for results
        paginator = Paginator(search_results, 3)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "posts/search_results.html", {
            "page_obj": page_obj,
            "categories": categories
        })
