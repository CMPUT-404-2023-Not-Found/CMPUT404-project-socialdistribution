# 2023-02-13
# author/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AuthorCreationForm, AuthorChangeForm
from .models import Author
# This code is modified from an article from Michael Herman on 2023-01-22 retrieved on 2023-02-15, to testdriven.io
# article here:
# https://testdriven.io/blog/django-custom-user-model/#forms
class AuthorAdmin(UserAdmin):
    add_form = AuthorCreationForm
    form = AuthorChangeForm
    model = Author

    # This code is from a question forum answer from Alexis N-o on 2015-07-02, retrieved on 2023-03-07, to stackoverflow.com
    # question forum answer here:
    # https://stackoverflow.com/questions/31194964/display-user-group-in-admin-interface
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)
    group.short_description = 'Groups'

    def node_id(self, user):
        return user.get_node_id()
    node_id.short_description = 'Node Id'

    date_hierarchy = 'updated_at'
    list_editable = ('is_active', )
    list_display = ('node_id', 'username', 'display_name', 'is_superuser', 'is_active', 'group', 'last_login', 'updated_at')
    list_filter = ('host', 'is_superuser', 'is_active', 'last_login')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'host', 'display_name', 'github', 'profile_image')}),
        ('Permissions', {'fields': ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'host',
                'password1', 'password2', 
                'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'
            )}
        ),
    )
    search_fields = ('id', 'username', 'host', 'display_name')
    ordering = ('id', 'username', 'host')

admin.site.register(Author, AuthorAdmin)
