from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin)
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from group.models import Group,GroupMember
from . import models
# Create your views here.
class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ("name","description")
    model = Group
class SingleGroup(generic.DetailView):
    model = Group
class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse("group:single",kwargs={"slug":self.kwargs.get("slug")})
    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user = self.request.user,group = group)
        except IntegrityError:
            messages.warning(self.request,(" WARNING: Already a member of the group {}".format(group.name)))
        else:
            messages.success(self.request,(" You are now a member of the group {}".format(group.name)))
        return super().get(request,*args,**kwargs)
class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse("group:single",kwargs={"slug":self.kwargs.get("slug")})
    def get(self,request,*args,**kwargs):
        try:
            membership = models.GroupMember.objects.filter(
            user=self.request.user,
            group__slug=self.kwargs.get("slug")).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,"You can't leave this group because you are not a member of this group")
        else:
            membership.delete()
            messages.success(self.request,"You have successfully left this group")
        return super().get(request,*args,**kwargs)
def search_groups(request):
    if request.method == "POST":
        searched = request.POST['searched']
        groups = models.Group.objects.filter(name__icontains=searched)
        # Use render() method to generate HTML page by combining
        # template and context
        return render(request,"group/search_group.html",{'searched':searched,'searched_groups':groups})
    else:
        searched = None
        learning_guides = LearningGuide.objects.all()
        indicators = Indicator.objects.all()
        return render(request,"learning_guides_app/search_learning_guides.html",{'searched':searched,'searched_learning_guides':learning_guides,'indicators':indicators,'homepage':False})
