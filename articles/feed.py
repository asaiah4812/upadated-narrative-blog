import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Articles

class LatestArticlesFeed(Feed):
    title = "My Articles"
    link = reverse_lazy('articles:articles_list')
    description = "New Articles of My Articles"
    
    def items(self):
        return Articles.published.all()[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.content), 30)
    
    def item_pubdate(self, item):
        return item.publish