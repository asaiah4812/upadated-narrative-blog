from django import template
from ..models import Articles
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag

def total_posts():
    return Articles.published.count()

@register.inclusion_tag('articles/article-list.html')
def show_latest_posts(count=5):
    latest_articles = Articles.published.order_by('-publish')[:count]
    return {'latest_articles': latest_articles}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))