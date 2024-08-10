from django.shortcuts import render, get_object_or_404, redirect
from .models import Articles, Comment
from .forms import SearchBook
# from accounts.models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, ArticlesForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from .filters import ArticlesFilter
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
import requests
from googleapiclient.discovery import build

# Create your views here.

def articles_list(request):
    articles = Articles.published.all()
    context = {
        'articles':articles,
    }
    return render(request, 'articles/article-list.html', context)

@login_required
def all_articles(request, tag_slug=None):
    article_filter = ArticlesFilter(request.GET, queryset=Articles.published.all())
    articles = article_filter.qs
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles_list = articles.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(articles, 5)
    page_number = request.GET.get('page', 1)
    try:
        articles = paginator.page(page_number)
    except PageNotAnInteger:
    # If page_number is not an integer deliver the first page
        articles = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)

    context = {
        'tag':tag,
        'filter': article_filter, 
        'articles': articles
    }
    return render(request, 'articles/all_articles.html', context)

@login_required
def articles_detail(request, year, month, day, article):
    article = get_object_or_404(Articles, slug=article, status=Articles.Status.PUBLISHED, publish__year=year, publish__month=month, publish__day=day)
    # List of active comments for this post
    comments = article.comments.filter(active=True)[:2]
    # # Form for users to comment
    form = CommentForm()
    # author = article.author
    # profile = author.profile if author.profile else None
    
    # List of similar posts
    article_tags_ids = article.tags.values_list('id', flat=True)
    similar_articles = Articles.published.filter(tags__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:2]
    context = {
        'article': article,
        'comments': comments, 
        'form':form, 
        'similar_articles':similar_articles
    }
    return render(request, 'articles/article_detail.html', context)

@login_required
def article_share(request, article_id):
    # Retrieve post by id
    article = get_object_or_404(Articles, id=article_id, status=Articles.Status.PUBLISHED)
    sent = False
    
    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            article_url = request.build_absolute_uri(
            article.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
            f"{article.title}"
            message = f"Read {article.title} at {article_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
            [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'articles/share.html', {'article': article, 'form':form, 'sent':sent })

@require_POST
def article_comment(request, article_id):
    article = get_object_or_404(Articles, id=article_id, status=Articles.Status.PUBLISHED)
    comment = None
    
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.article = article
        # Save the comment to the database
        comment.save()
    return render(request, 'articles/comment.html', {
            'article': article, 
            'form': form, 
            'comment': comment
            })
    
    
def like_article(request, pk):
    article = get_object_or_404(Articles, id=pk)
    
    if article.author != request.user:    
        article.likes.add(request.user)
    return redirect('article', article.id)
def create_articles(request):
    if request.method == 'POST':
        form = ArticlesForm(request.POST, request.FILES or None)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user 
            article.save()
            messages.success(request, ('Successfully created article!'))
            return redirect('articles:articles_list')
        else:
            messages.info(request, 'something went wrong')
    else:
        form = ArticlesForm()
    return render(request,'articles/create.html',{'form':form})


def update_articles(request, pk):
    article = Articles.published.get(id=pk)
    form = ArticlesForm()
    if request.method == 'POST':
        form = ArticlesForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:articles_list')
    else:
        form = ArticlesForm(instance=article)
    return render(request, 'articles/update.html', {'form': form})
        
def delete_articles(request, pk):
    article = Articles.published.get(id=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles:articles_list')


def books(request):
    YOUR_API_KEY = "AIzaSyAjmAgT3Q4tHYtSKiUkhpvw5sbVhEB765Y"
    if request.method == 'POST':
        form = SearchBook(request.POST)
        text = request.POST['text']
        url = f"https://www.googleapis.com/books/v1/volumes?q={text}&key={YOUR_API_KEY}"
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {
                'form': form,
                'results':result_list
            }
    
        return render(request, 'articles/books.html', context)  # Show error template
    else:
        url = f"https://www.googleapis.com/books/v1/volumes?q=programming&key={YOUR_API_KEY}"
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
        return render(request, 'articles/books.html', {'results':result_list})
    



