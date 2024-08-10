from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path('', views.articles_list, name='articles_list'),
    path('tag/<slug:tag_slug>/', views.articles_list, name='articles_list_by_tag'),
    # path('add-like/<int:pk>/', views.add_like, name='add_like'),
    path('books', views.books, name='books'),
    path('article/<slug:article_id>/like', views.like_article, name="like"),
    path('all-articles/', views.all_articles, name='all_articles'),
    path('create-article/', views.create_articles, name='create_article'),
    path('update-article/<int:pk>/', views.update_articles, name='update_article'),
    path('<int:year>/<int:month>/<int:day>/<slug:article>/', views.articles_detail, name='articles_detail'),
    path('<int:article_id>/share/', views.article_share, name='article_share'),
    path('<int:article_id>/comment/', views.article_comment, name='article_comment'),
    path('delete-article/<int:pk>/', views.delete_articles, name='delete_articles'),
]
