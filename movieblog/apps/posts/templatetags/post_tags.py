from django import template

from movieblog.apps.posts.models import Category

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.order_by()
