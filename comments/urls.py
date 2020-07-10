from django.urls import path

from .views import CommentCreateView, CommentUpdateView, CommentDeleteView
# from .views import postComment

urlpatterns = [
    path('new/', CommentCreateView.as_view(), name='comment-create'),
    path('<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete')
]
