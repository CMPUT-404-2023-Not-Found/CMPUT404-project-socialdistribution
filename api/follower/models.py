from django.db import models
from django.apps import apps
from author.models import Author


class Follower(models.Model):
    # Identification fields
    follower_node_id              = models.URLField(blank=False, null=False, max_length=128, db_index=True, verbose_name='author who is following the followee')
    followee              = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='followee')

    # Modification fields
    followed_at           = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Followed At')

    def __str__(self):
        return f'{self.follower_node_id} follows {self.followee}'

    # 
    #  This code was adapted from a post from Jens on 2010-02-04, retrieved on 2023-03-13, 
    #  forum here:
    #  https://stackoverflow.com/a/2201687
    # */
    class Meta:
        unique_together = ('follower_node_id', 'followee')