# 2023-02-16
# post/admin.py

from django.contrib import admin

from .models import Post

class PostAdmin(admin.ModelAdmin):
    model = Post
    def node_id(self, obj):
        return obj.get_node_id()
    node_id.short_description = 'Node Id'

    list_display = ('node_id', 'author', 'title', 'description', 'content_type', 'unlisted', 'visibility', 'published', 'updated_at')
    list_filter = ('author', 'content_type', 'updated_at')

admin.site.register(Post, PostAdmin)
