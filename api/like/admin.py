# 2023-03-18
# api/like/admin.py

from django.contrib import admin
from like.models import Like

class LikeAdmin(admin.ModelAdmin):
    model = Like

    def post_node_id(self, obj):
        return obj.post.get_node_id() if obj.post else None
    post_node_id.short_description = 'Post Node Id'

    def post_title(self, obj):
        return obj.post.title if obj.post else None
    post_title.short_description = 'Post Title'

    def comment_node_id(self, obj):
        return obj.comment.get_node_id() if obj.comment else None
    comment_node_id.short_description = 'Comment Node Id'

    def comment_content(self, obj):
        return obj.comment.comment if obj.comment else None
    comment_content.short_description = 'Comment Content'

    empty_value_display = '-empty-'
    list_display = ('summary', 'author', 'post_node_id', 'post_title', 'comment_node_id', 'comment_content', 'liked_at')
    list_filter = ('author', 'post__id', 'comment__id', 'liked_at')
    search_fields = ('author', 'summary', 'post__title', 'comment__comment')
    ordering = ('author', 'liked_at')

admin.site.register(Like, LikeAdmin)
