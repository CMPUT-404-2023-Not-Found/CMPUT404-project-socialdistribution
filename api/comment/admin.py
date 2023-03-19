# 2023-03-02
# comment/admin.py

from django.contrib import admin

from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    model = Comment

    def post_id(self, obj):
        return obj.post.get_node_id()
    post_id.short_description = 'Parent Post Id'

    def node_id(self, obj):
        return obj.get_node_id()
    node_id.short_description = 'Node Id'

    list_display = ('node_id', 'comment', 'content_type', 'post_id', 'author', 'published')
    list_filter = ('post', 'author', 'content_type')
    search_fields = ('id', 'author', 'comment')
    ordering = ('id', )

admin.site.register(Comment, CommentAdmin)
