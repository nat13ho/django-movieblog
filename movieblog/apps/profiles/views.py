from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from movieblog.apps.posts.models import Category, Post
from .forms import ProfileForm


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'profiles/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by()
        return context

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        if self.request.user.id == user_id:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class FavouritePostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'profiles/profile_post_list.html'

    def get_queryset(self):
        user = self.request.user
        posts = user.profile.posts.all()
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by()
        return context


@login_required
def add_to_bookmarks(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    next_url = request.POST.get('next')
    if post and user:
        user.profile.posts.add(post)
        user.save()
        return redirect(next_url)
    else:
        return redirect(reverse('home'))


@login_required
def remove_from_bookmarks(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    next_url = request.POST.get('next')
    if post and user:
        user.profile.posts.remove(post)
        user.save()
        return redirect(next_url)
    else:
        return redirect(reverse('home'))


@login_required
def update_profile(request, pk):
    user = request.user
    if user.pk == pk:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                user.username = data['username']
                if data['image']:
                    user.profile.image = request.FILES['image']
                user.profile.is_subscribed = data['is_subscribed']
                user.save()
                return redirect(reverse('profiles:profile_details', kwargs={'pk': user.pk}))
            else:
                return render(request, 'profiles/profile_update.html', {'form': form})
        else:
            form = ProfileForm(initial={
                'username': user.username,
                'image': user.profile.image,
                'is_subscribed': user.profile.is_subscribed}
            )
            return render(request, 'profiles/profile_update.html', {'form': form})
    else:
        return HttpResponseForbidden()
