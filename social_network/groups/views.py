from django.shortcuts import render
from django.db import IntegrityError
# Create your views here.

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                    PermissionRequiredMixin)
from django.urls import reverse
from django.views import  generic

from django.contrib import messages

from . import models

from django.shortcuts import get_object_or_404


from groups.models import Group,GroupMember

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = {'description','name'}
    model = Group

class SingleGroup(generic.DetailView):
    model = Group


class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        print(self.kwargs.get('slug'))
        return reverse("groups:single",kwargs={'slug':self.kwargs.get('slug')})

    # get is http method(so this furnction is called when get request is sent)
    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request, "Warning already a member!")
        else:
            messages.success(self.request,'You are a memeber now.')

        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
         return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        try:
            membership = GroupMember.objects.filter(user= self.request.user, group__slug=self.kwargs.get('slug')).get()
        except GroupMemeber.DoesNotExist:
            messages.warning(self.request,"Sorry you are'nt in this group!")
        else:
            membership.delete()
            messages.success(self.request,'You have left the group!')

        return super().get(request,*args,**kwargs)
