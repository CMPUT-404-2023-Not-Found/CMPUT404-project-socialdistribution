# 2023-02-18
# inbox/admin.py

from django.contrib import admin

from .models import Inbox

class InboxAdmin(admin.ModelAdmin):
    model = Inbox
    list_display = ('author', 'summary', 'sender_author_id', 'type', 'received_at')
    list_filter = ('author', )
admin.site.register(Inbox, InboxAdmin)
