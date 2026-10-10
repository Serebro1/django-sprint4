from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


# Create your views here.
def get_published_posts():
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    )


def index(request):
    post_list = get_published_posts().select_related(
        'category', 'location', 'author'
    )[:5]
    return render(request, 'blog/index.html', {'post_list': post_list})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_published_posts().filter(
        category=category
    ).select_related('category', 'location', 'author')
    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': post_list,
    })


def post_detail(request, post_id):
    post = get_object_or_404(
        get_published_posts().select_related('category', 'location', 'author'),
        id=post_id,
    )
    return render(request, 'blog/detail.html', {'post': post})
