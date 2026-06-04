from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="media/users/%Y/%m/%d/", blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.username
    
class Post(models.Model):
    
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
        
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey("Post", related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey("CustomUser", related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user} on {self.post}"