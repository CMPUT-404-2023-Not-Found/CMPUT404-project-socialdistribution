# 2023-02-16
# post/admin.py

from django.contrib import admin

from .models import Post

class PostAdmin(admin.ModelAdmin):
    model = Post
    def node_id(self, obj):
        return obj.get_node_id()
    node_id.short_description = 'Node Id'

    def author_name(self, obj):
        return obj.author.display_name if obj.author.display_name else obj.author.username
    author_name.short_description = 'Author'

    list_display = ('node_id', 'author_name', 'title', 'description', 'content_type', 'visibility', 'unlisted', 'updated_at')
    list_filter = ('id', 'title', 'content_type', 'updated_at')
    search_fields = ('id', 'title')
    ordering = ('id', 'title')

admin.site.register(Post, PostAdmin)
