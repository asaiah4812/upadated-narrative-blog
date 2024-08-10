from django.contrib.sitemaps import Sitemap
from .models import Articles

class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Articles.published.all()
    def lastmod(self, obj):
        return obj.updated
