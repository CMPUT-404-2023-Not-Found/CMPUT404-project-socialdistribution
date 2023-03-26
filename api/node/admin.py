# 2023-03-07
# node/admin.py

from django.contrib import admin

from .models import Node

class NodeAdmin(admin.ModelAdmin):
    model = Node
    list_display = ('host', 'username', 'password', 'api_path')
    list_display_links = None
    list_editable = ('host', 'username', 'password', 'api_path')
    list_filter = ('host',)
    search_fields = ('host', 'username')
    ordering = ('host',)

admin.site.register(Node, NodeAdmin)
