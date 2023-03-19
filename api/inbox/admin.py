# 2023-02-18
# inbox/admin.py

from django.contrib import admin

from .models import Inbox

class InboxAdmin(admin.ModelAdmin):
    model = Inbox
    def inbox_owner(self, obj):
        return obj.author.display_name if obj.author.display_name else obj.author.username
    inbox_owner.short_description = 'Inbox Owner'

    date_hierarchy = 'received_at'
    list_display = ('inbox_owner', 'type', 'summary', 'object_id', 'sender_author_id', 'received_at')
    list_display_links = ('summary', )
    list_filter = ('author', 'sender_author_id', 'type', 'received_at')
    search_fields = ('summary', 'sender_author_id', 'author__username', 'author__display_name')
    ordering = ('id', 'received_at')
admin.site.register(Inbox, InboxAdmin)
