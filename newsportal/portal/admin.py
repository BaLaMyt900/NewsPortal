from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'type', 'post_time']
    list_filter = ['categories']


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'rating']


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'post_count', 'numbers_of_posts']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['prewiew', 'user', 'post', 'date', 'rating']



admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PortalUser, UserAdmin)


