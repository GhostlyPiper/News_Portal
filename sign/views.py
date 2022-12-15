from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView
from .models import BaseRegisterForm
from .basic_forms import UpdateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from news.models import Author


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def log_in_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(authorUser=user)
    return redirect('/news/my_posts')


@login_required
def log_out_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if request.user.groups.filter(name='authors').exists():
        authors_group.user_set.remove(user)
        d = Author.objects.get(authorUser=user)
        d.delete()
    return redirect('/')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile_update.html'
    form_class = UpdateProfileForm
    success_url = '/'
    success_message = 'User profile updated successfully.'

    def get_object(self, **kwargs):
        return self.request.user
