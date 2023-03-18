# 2023-03-17
# api/like/models.py

from django.db import models
from post.models import Post
from comment.models import Comment

class Like(models.Model):
    class W3ContextChoices(models.TextChoices):
        W3_AS=('https://www.w3.org/ns/activitystreams', 'W3 Activity Streams')
    
    # Identification Fields
    post                = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    comment             = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    author              = models.URLField(max_length=128, db_index=True, verbose_name="Who liked it", null=False, blank=False)

    # Content Fields
    context             = models.URLField(choices=W3ContextChoices.choices, default=W3ContextChoices.W3_AS, max_length=128)
    summary             = models.CharField(max_length=128)

    # Modification Fields
    liked_at            = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Liked At')

    def __str__(self):
        if self.summary:
            return f'{self.summary}'
        elif self.post:
            return f'{self.author} liked post {self.post.id}'
        else:
            return f'{self.author} liked comment {self.comment.id}'

    '''
    Allow a user to like a post or comment only once, add a unique_together constraint to Like model that
    ensures that the combination of author, post, and comment fields is unique. 
    This way, if a user tries to create a new like with the same author, post, and comment values as an existing like, 
    the database will raise an IntegrityError and the new like will not be created.

    (author1, post1, null) like1
    (author1, post1, null) like2 # error => (author1, null, comment1) like2 
    
    '''
    # 
    #  This code was adapted from a post from Jens on 2010-02-04, retrieved on 2023-03-13, 
    #  forum here:
    #  https://stackoverflow.com/a/2201687
    # */
    class Meta:
        unique_together = ('author', 'post', 'comment')
