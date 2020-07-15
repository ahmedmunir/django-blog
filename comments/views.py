from django.shortcuts import render, reverse

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, View

from posts.models import Post
from comments.models import Comment

from django.http import HttpResponse, JsonResponse

# Create your views here.

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
        Create new Comment.
    """
    def post(self, request, *args, **kwargs):
        #Get data we need about comment
        comment = request.POST.get('comment')
        post = Post.objects.get(pk=kwargs.get('post_id'))
        user = request.user

        #Add comment to database.
        new_comment = Comment.objects.create(owner=user, post=post, text=comment)
        
        #Return data to client-side
        return JsonResponse({
            "result": "Success",
            "url": new_comment.owner.profile.image.url,
            "user_posts": reverse('user-posts', kwargs={"username":new_comment.owner.username}),
            "username": new_comment.owner.username,

            # we can't format time at client side because it is not data injected from
            # django but JSON data, so we will format those data at server side.
            "date": new_comment.date_posted.strftime("%B %d, %Y, %H:%M %p"),
            
            "text": new_comment.text,
            "comment_update": reverse('comment-update', 
                kwargs={
                        "post_id": new_comment.post.id,
                        "pk": new_comment.pk

                    }
            ),
            "comment_delete": reverse('comment-update', 
                kwargs={
                        "post_id": new_comment.post.id,
                        "pk": new_comment.pk

                    }
            )
        })


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
        Update Comment after execute middleware UserPassesTestMixin to make sure that
        the owner of the comment is the requester.
    """
    
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
    """
        Delete Comment after execute middleware UserPassesTestMixin to make sure that
        the owner of the comment is the requester.
    """
    
    model = Comment

    def test_func(self):
        self.comment = self.get_object()

        if self.comment.owner == self.request.user or self.comment.post.author == self.request.user:
            return True
        return False

    # where to redirect after successfully delete comment
    def get_success_url(self):
        return reverse('post-detail', args=[self.get_object().post.id])