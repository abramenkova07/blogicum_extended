from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

from .constants import SHOWED_ITEMS
from .models import Comment, Category, Post


def all_posts_queryset():
    return Post.objects.select_related(
        'category',
        'location',
        'author').order_by('-pub_date')


def filtered_posts_queryset():
    return Post.objects.select_related(
        'category',
        'location',
        'author').filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
            ).annotate(
                comment_count=Count('commented_post')
            ).order_by('-pub_date')


def all_comments_queryset():
    return Comment.objects.select_related(
        'author',
        'post')


def published_category_queryset():
    return Category.objects.all().filter(
        is_published=True)


def paginate_queryset(queryset, request):
    paginator = Paginator(queryset, SHOWED_ITEMS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
