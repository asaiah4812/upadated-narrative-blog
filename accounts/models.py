from django.db import models
from django.conf import settings

# Create your models here.





class Profile(models.Model):
    CARRIER_CHOICES = [
        ('Software Enginneer', 'Software Enginneer'),
        ('Fullstack Enginneer', 'Fullstack Enginneer'),
        ('Frontend Developer', 'Frontend Developer'),
        ('Mobile App Developer', 'Mobile App Developer'),
        ('Backend Developer', 'Backend Developer'),
        ('Product Designer', 'Product Designer'),
        ('Product Manager', 'Product Manager'),
        ('System Analyst', 'System Analyst'),
        ('Digital Marketer', 'Digital Marketer'),
        ('Machine Learning Engineer', 'Machine Learning Engineer'),
        ('Data Scientist', 'Data Scientist'),
        ('Network Enginneer', 'Network Enginneer'),
        ('Cybersecurity Specialist', 'Cybersecurity Specialist'),
        ('Security Engineer', 'Security Engineer'),
        ('Security Analyst', 'Security Analyst'),
        ('Database Administrator', 'Database Administrator'),
        ('Systems Administrator', 'Systems Administrator'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    carrier = models.CharField(max_length=25, choices=CARRIER_CHOICES)
    DEFAULT_PROFILE_PICTURE = 'static/images/profile.jpg'
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', default=DEFAULT_PROFILE_PICTURE,  blank=True, null=True)
    
    def __str__(self):
        return f'Profile of {self.user.username}'
