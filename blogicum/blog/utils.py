from django.core.paginator import Paginator

from .constants import SHOWED_ITEMS


def paginating(object, request):
    paginator = Paginator(object, SHOWED_ITEMS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
