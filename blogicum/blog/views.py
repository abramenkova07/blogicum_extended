from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from django.utils import timezone

from .constants import SHOWED_ITEMS
from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post
from .utils import paginating

# Filtered posts
filtered_posts = Post.objects.select_related(
    'category',
    'location',
    'author'
).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
).annotate(
            comment_count=Count('commented_post')
).order_by('-pub_date')

# All posts
all_posts = Post.objects.select_related('location',
                                        'author',
                                        'category')

# All_comments
all_comments = Comment.objects.select_related('author',
                                              'post')


class PostListView(ListView):
    model = Post
    queryset = filtered_posts
    paginate_by = SHOWED_ITEMS
    template_name = 'blog/index.html'


def post_detail(request, pk):
    author = get_object_or_404(all_posts, pk=pk).author
    if author == request.user:
        post = get_object_or_404(all_posts, pk=pk)
    else:
        post = get_object_or_404(filtered_posts, pk=pk)
    return render(request, 'blog/detail.html',
                  {'form': CommentForm(),
                   'comments':
                   post.commented_post.select_related('author'),
                   'post': post})


def category_posts(request, category_slug):
    chosen_category = get_object_or_404(
        Category.objects.all().filter(
            is_published=True), slug=category_slug
    )
    chosen_posts = chosen_category.category_posts.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    ).annotate(
        comment_count=Count('commented_post')
    ).order_by('-pub_date')
    page_obj = paginating(chosen_posts, request)
    return render(request, 'blog/category.html', {
        'category': chosen_category, 'page_obj': page_obj})


def show_profile(request, username):
    profile = get_object_or_404(get_user_model(),
                                username=username)
    if username == request.user.username:
        chosen_posts = profile.author_posts.all(
        ).annotate(comment_count=Count('commented_post')).order_by('-pub_date')
    else:
        chosen_posts = profile.author_posts.filter(
            Q(is_published=True)
            & Q(category__is_published=True)
            & Q(pub_date__lte=timezone.now())).annotate(
            comment_count=Count('commented_post')
        ).order_by('-pub_date')
    page_obj = paginating(chosen_posts, request)
    return render(request, 'blog/profile.html',
                  {'profile': profile, 'page_obj': page_obj})


@login_required
def profile_edit(request):
    form = UserForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user)
    return render(request, 'blog/user.html', {'form': form})


@login_required
def post_modify(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(all_posts, pk=pk)
        if instance.author != request.user:
            return redirect('blog:post_detail', pk)
    else:
        instance = None
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        if '/edit/' in request.path:
            return redirect('blog:post_detail', pk)
        elif '/create/' in request.path:
            return redirect('blog:profile', request.user)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def comment_modify(request, pk, id=None):
    post = get_object_or_404(filtered_posts, pk=pk)
    if id is not None:
        comment = get_object_or_404(
            all_comments,
            post=pk, pk=id,
            author=request.user)
    else:
        comment = None
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', pk)
    return render(request, 'blog/comment.html', {'form': form,
                                                 'post': post,
                                                 'comment': comment})


@login_required
def post_delete(request, pk):
    instance = get_object_or_404(all_posts, pk=pk, author=request.user)
    form = PostForm(instance=instance)
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:profile', request.user)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def comment_delete(request, pk, id):
    comment = get_object_or_404(
        all_comments, post=pk,
        id=id,
        author=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', pk)
    return render(request, 'blog/comment.html', {'comment': comment})
