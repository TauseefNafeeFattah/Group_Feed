from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
## know about this
from braces.views import SelectRelatedMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from django.contrib.auth.decorators import login_required

from . import models,forms
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()

class PostList(SelectRelatedMixin,generic.ListView):
    # the list of post related to the user and the group
    model = models.Post
    select_related = ("user","group")

class UserPosts(generic.ListView):
    # all the post of the user
    model = models.Post
    template_name = "post/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
            username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"]=self.post_user
        return context

class PostDetail(SelectRelatedMixin,generic.DetailView):
    # the details of a post
    model = models.Post
    select_related = ("user","group")

    def get_queryset(self):
        # know about this
        queryset = super().get_queryset()
        return queryset.filter(
        user__username__iexact=self.kwargs.get("username")
        )
class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields = ('message','group')
    model = models.Post

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ("user","group")
    success_url = reverse_lazy("home")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,"Post Deleted")
        return super().delete(*args,**kwargs)

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(models.Post,pk = pk)
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post:single',username=post.user.username,pk = post.pk)
    else:
        form = forms.CommentForm()
    return render(request,'post/comment_form.html',{'form':form})
@login_required
def remove_comment(request,pk):
    comment = get_object_or_404(models.Comment,pk = pk)
    post_pk = comment.post.pk
    post_name = comment.post.user.username
    comment.delete()
    return redirect('post:single',username=post_name,pk = post_pk)
