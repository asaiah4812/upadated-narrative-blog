from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Articles.Status.PUBLISHED)
    
class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Articles.Status.DRAFT)

# class Author(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField()

#     def __str__(self):
#         return self.user.username
    
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name

class Articles(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    content = CKEditor5Field('content', config_name='extends')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    publish = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likedposts', through="LikedPost")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='article_images/')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()
    draft = DraftManager()
    tags = TaggableManager()
    
    class Meta:
        ordering = ['-publish']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        indexes = [
            models.Index(fields=['-publish']),
            ]
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def get_absolute_url(self):
        return reverse('articles:articles_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

class LikedPost(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['created']
        indexes = [
        models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.article}'
    

    
    