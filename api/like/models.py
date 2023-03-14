
from django.db import models
from author.models import Author
from post.models import Post
from comment.models import Comment


class Like(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, verbose_name="who liked it")

    # summary = models.CharField(max_length=128, blank=True, null=True, verbose_name='Summary of the like')

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
    class Meta:
        unique_together = ('author', 'post', 'comment')