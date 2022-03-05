from django.urls import reverse
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin)
from post.models import Post
from group.models import Group
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

class TestPage(TemplateView):
    template_name = "tests.html"
class ThanksPage(TemplateView):
    template_name = "thanks.html"
class HomePage(TemplateView):
    template_name = "index.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["posts_list"]=Post.objects.filter(group__members__pk=self.request.user.pk).order_by("-created_at")
        context["user_groups"]=Group.objects.filter(members__pk=self.request.user.pk)
        context["all_groups"]=Group.objects.all()
        return context
