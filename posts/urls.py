from django.urls import path

from . import views

from .views import (
    HomeView,
    PostsListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    SearchView
)

urlpatterns = [
    path('', HomeView.as_view(), name='blog-home'),
    path('blog/', PostsListView.as_view(), name="blog-posts"),
    path('search/', SearchView.as_view(), name="search-posts"),
    path('about/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

]


