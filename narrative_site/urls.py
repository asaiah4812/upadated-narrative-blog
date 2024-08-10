from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from articles.sitemaps import ArticleSitemap

sitemaps = {
    'articles': ArticleSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('articles.urls', namespace='articles')),
    path('accounts/', include('accounts.urls')),
    path('inspiration/', include('inspiration.urls', namespace='inspiration')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    ]