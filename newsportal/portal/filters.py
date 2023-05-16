from django_filters import FilterSet
from .models import Post



class PostFilter(FilterSet):
    class Meta:
        model = Post
        # fields = ('author__user__username', 'type', 'categories', 'post_time')
        fields = {
            'author__user__username': ['icontains'],
            'type': ['exact'],
            'categories': ['exact'],
            'post_time': ['date__lte']
        }