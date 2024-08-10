from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Inspiration(models.Model):
    language = (
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('Python', 'Python'),
        ('Java scripts', 'Java scripts'),
        ('Java', 'Java'),
        ('Kotlin', 'Kotlin'),
        ('C++', 'C++'),
        ('C#', 'C#'),
        ('Ruby', 'Ruby'),
        ('Swift', 'Swift'),
        ('Solidity', 'Solidity'),
        ('Dart', 'Dart'),
    ) 
    title = models.CharField(max_length=100)
    builder = models.ForeignKey(User, on_delete=models.CASCADE)
    source_code = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250)
    live_demo = models.CharField(max_length=50)
    description = models.TextField()
    programmingLg = models.CharField(max_length=25, choices=language)
    image = models.ImageField(upload_to='inspiration_images/')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
            ]
        
    def get_absolute_url(self):
        return reverse('inspiration:inspiration_detail', args=[self.slug])
    
    
    def __str__(self):
        return self.title

