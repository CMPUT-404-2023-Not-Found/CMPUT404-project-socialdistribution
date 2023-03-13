
from django.db import models
from author.models import Author
from post.models import Post
from comment.models import Comment


class Like(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, verbose_name="who liked it")

    summary = models.CharField(max_length=128, blank=True, null=True, verbose_name='Summary of the like')

    def __str__(self):
        summary = ""
        if self.post:
            summary = f'{self.user} liked post {self.post.id}'
            return summary
        else:
            summary = f'{self.user} liked comment {self.comment.id}'
            return summary

