from django.db import models
from django.apps import apps
from author.models import Author

# Create your models here.
class Follower(models.Model):
    # Identification fields
    follower              = models.URLField(primary_key= True, blank=False, null=False, max_length=128, verbose_name='author who is following the followee')
    # QUESTION: What does related_name mean?
    followee              = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='followee')

    # Modification fields
    # auto_now: for saving the time every time the field is saved. Useful for last modified
    # auto_now_add: for saving the time only when the object is created
    followed_at           = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Followed At')

    def __str__(self):
        return f'{self.follower} follows {self.followee}'


'''  
Followers.objects.all().count()
class FollowerCount(models.Model):
    # Identification fields
    author              = models.ForeignKey(to='author.Author', on_delete=models.CASCADE, related_name='author')
    count               = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.author} has {self.count} followers'
'''