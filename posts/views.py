from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .models import Post, Comment
from .forms import CommentForm


class HomeView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/index.html'

    def get_queryset(self):
        posts = Post.objects.select_related('category')[:6]
        return posts

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        return context


class PostListView(HomeView):
    paginate_by = 12
    template_name = 'posts/post_list.html'
    ordering = '-pub_date'

    def get_queryset(self):
        default_sort = self.get_ordering()
        category = self.request.GET.get('category')
        search_string = self.request.GET.get('search_string')
        order_by_date = self.request.GET.get('pub_date')
        order_by_title = self.request.GET.get('title')
        order_by_popularity = self.request.GET.get('popularity')
        sort_order = order_by_date or order_by_title or default_sort

        if category:
            posts = Post.objects\
                .filter(category_id=int(category))\
                .select_related('category')\
                .order_by(sort_order)
        elif search_string:
            posts = Post.objects\
                .filter(Q(title__icontains=search_string) | Q(content__icontains=search_string))\
                .select_related('category')\
                .order_by(sort_order)
        elif order_by_popularity:
            if order_by_popularity == 'asc':
                posts = Post.objects\
                    .annotate(num_profile=Count('profile'))\
                    .select_related('category')\
                    .order_by('-num_profile')
            else:
                posts = Post.objects\
                    .annotate(num_profile=Count('profile'))\
                    .select_related('category')\
                    .order_by('num_profile')
        else:
            posts = Post.objects.select_related('category').order_by(sort_order)
        return posts

    def get_context_data(self, *args, **kwargs):
        order_by_date = self.request.GET.get('pub_date', '-pub_date')
        order_by_title = self.request.GET.get('title', 'title')
        order_by_popularity = self.request.GET.get('popularity', 'desc')
        context = super().get_context_data(*args, **kwargs)
        context['pub_date'] = '-pub_date' if order_by_date == 'pub_date' else 'pub_date'
        context['title'] = 'title' if order_by_title != 'title' else '-title'
        context['popularity'] = 'asc' if order_by_popularity != 'asc' else 'desc'
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/post_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['comment_form'] = CommentForm()
        return context


@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
        form = CommentForm(request.POST)

        if post and user:
            if form.is_valid():
                data = form.cleaned_data
                Comment.objects.create(content=data.get('content'), post=post, user=user)

    return redirect(reverse('posts:post_details', kwargs={'pk': post_id}))


@login_required
def remove_comment(request, post_id, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=comment_id)
        user = request.user

        if comment.user == user or user.is_superuser:
            comment.delete()
        else:
            return HttpResponseForbidden()

    return redirect(reverse('posts:post_details', kwargs={'pk': post_id}))
