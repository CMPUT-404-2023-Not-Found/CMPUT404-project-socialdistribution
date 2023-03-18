# 2023-02-16
# post/admin.py

from django.contrib import admin

from .models import Post, Category

class PostAdmin(admin.ModelAdmin):
    model = Post

    def categories(self, obj):
        return obj.get_category_item_list()
    categories.short_description = 'Categories'

    list_display = ('id', 'description', 'categories')
    list_filter = ('author', )

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
