from rest_framework import viewsets
from portal.rest_api.serializers import *


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'pk'


class NewsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(type='N')
    serializer_class = PostSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Post.objects.all()
        author_id = self.request.query_params.get('author_id', None)
        if author_id is not None:
            qs = qs.filter(author=author_id)
        return qs


class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(type='A')
    serializer_class = PostSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Post.objects.all()
        author_id = self.request.query_params.get('author_id', None)
        if author_id is not None:
            qs = qs.filter(author=author_id)
        return qs


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Comment.objects.all()
        user = self.request.query_params.get('user_id', None)
        post = self.request.query_params.get('post_id', None)
        if user is not None:
            qs = qs.filter(user=user)
        if post is not None:
            qs = qs.filter(post=post)
        return qs


class PortalUserViewSet(viewsets.ModelViewSet):
    queryset = PortalUser.objects.all()
    serializer_class = PortalUserSerializer
    lookup_field = 'pk'
