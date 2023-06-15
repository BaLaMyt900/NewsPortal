from portal.models import Author, Post, Comment, PortalUser, Category
from rest_framework import serializers


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['pk', 'user', 'rating', ]
        read_only_fields = ['pk', 'user']


class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategoriesSerializer(many=True)
    class Meta:
        model = Post
        lookup_field = 'pk'
        fields = ['pk', 'author', 'type', 'categories', 'post_time', 'title', 'text', ]
        read_only_fields = ['pk', 'author']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        lookup_field = 'pk'
        fields = ['pk', 'user', 'date', 'post', 'text', 'rating', ]
        read_only_fields = ['pk', 'user']


class PortalUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PortalUser
        lookup_field = 'pk'
        fields = ['pk', 'username', 'rating']
        read_only_fields = ['pk']
