from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserDetails(models.Model):
    username = models.CharField(max_length=70)
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=70) 
    role = models.CharField(max_length=70)

    def  __str__(self):
        return self.username


class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/',default="")
    content = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.title[:50]


