from django_filters import FilterSet
from portal.models import Post



class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'author__user__username': ['exact'],
            'type': ['exact'],
            'categories': ['exact'],
            'post_time': ['date__lte']
        }