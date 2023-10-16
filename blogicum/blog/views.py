from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)
from django.views.generic.edit import ModelFormMixin
from django.urls import reverse
from django.utils import timezone

from .constants import SHOWED_ITEMS
from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post
from .utils import (all_comments_queryset,
                    all_posts_queryset,
                    filtered_posts_queryset,
                    paginate_queryset,
                    published_category_queryset)


class PostListView(ListView):
    model = Post
    paginate_by = SHOWED_ITEMS
    template_name = 'blog/index.html'
    queryset = filtered_posts_queryset()


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=all_posts_queryset()):
        instance = get_object_or_404(queryset, pk=self.kwargs['post_id'])
        if instance.author == self.request.user:
            return instance
        return get_object_or_404(
            filtered_posts_queryset(), pk=self.kwargs['post_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.commented_post.select_related(
            'author')
        context['post'] = self.object
        return context


class PostMixin:
    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PostMixin, UpdateView):
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={
            'post_id': self.kwargs['post_id']})


class PostDeleteView(LoginRequiredMixin, PostMixin, DeleteView,
                     ModelFormMixin):
    fields = ('text', 'title', 'pub_date', 'location', 'image')
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    queryset = published_category_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chosen_posts = self.object.category_posts.filter(
            is_published=True,
            pub_date__lte=timezone.now()
        ).annotate(
            comment_count=Count('commented_post')
        ).order_by('-pub_date')
        page_obj = paginate_queryset(chosen_posts, self.request)
        context['page_obj'] = page_obj
        return context


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={
            'post_id': self.kwargs['post_id']})


class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateView):
    chosen_post = None
    form_class = CommentForm

    def get_object(self, queryset=filtered_posts_queryset()):
        instance = get_object_or_404(
            queryset,
            pk=self.kwargs['post_id'])
        return instance

    def dispatch(self, request, *args, **kwargs):
        self.chosen_post = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.chosen_post
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, CommentMixin, UpdateView):
    form_class = CommentForm

    def get_object(self, queryset=all_comments_queryset()):
        instance = get_object_or_404(
            queryset,
            post=self.kwargs['post_id'],
            pk=self.kwargs['comment_id'])
        return instance

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            filtered_posts_queryset(),
            pk=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):

    def get_object(self, queryset=all_comments_queryset()):
        instance = get_object_or_404(
            queryset,
            post=self.kwargs['post_id'],
            pk=self.kwargs['comment_id'])
        return instance

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProfileDetailView(DetailView):
    model = get_user_model()
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object == self.request.user:
            chosen_posts = self.object.author_posts.all(
            ).annotate(comment_count=Count('commented_post')).order_by(
                '-pub_date')
        else:
            chosen_posts = self.object.author_posts.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now()).annotate(
                    comment_count=Count('commented_post')
            ).order_by('-pub_date')
        page_obj = paginate_queryset(chosen_posts, self.request)
        context['page_obj'] = page_obj
        context['profile'] = self.object
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'blog/user.html'
    form_class = UserForm

    def get_object(self, queryset=get_user_model().objects.all()):
        instance = get_object_or_404(
            queryset,
            username=self.request.user)
        return instance

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})
