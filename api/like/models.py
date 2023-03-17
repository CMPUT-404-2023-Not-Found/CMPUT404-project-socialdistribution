
from django.db import models
from author.models import Author
from post.models import Post
from comment.models import Comment


class Like(models.Model):
    class W3ContextChoices(models.TextChoices):
        W3_AS=('https://www.w3.org/ns/activitystreams', 'W3 Activity Streams')
    
    post                = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    comment             = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    author              = models.ForeignKey(to=Author, on_delete=models.CASCADE, verbose_name="who liked it")
    context             = models.URLField(choices=W3ContextChoices.choices, default=W3ContextChoices.W3_AS, max_length=128)

    def __str__(self):
        if self.post:
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
