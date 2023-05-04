from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return 'Автор: ' + self.user.username

    def update_rating(self):
        author_posts = Post.objects.filter(author_id=self.id)
        posts_rating = sum([author_post.rating for author_post in author_posts])
        posts_rating = posts_rating * 3 if posts_rating != 0 else posts_rating
        comment_rating = sum(Comment.objects.filter(user_id=self.user.id))
        post_comment_rating = sum([post_comment.rating
                                   for post_comment in Comment.objects.filter(post_id__in=author_posts.values('id'))])

        self.rating = posts_rating + comment_rating + post_comment_rating
        self.save()

    class Meta:
        verbose_name = 'Автора'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    types = [
        ('A', 'Статья'),
        ('N', 'Новость')
    ]
    type = models.CharField(max_length=1, choices=types)
    post_time = models.DateTimeField(datetime.now())
    __categories = [(name['id'], name['name']) for name in Category.objects.all().values('id', 'name')]
    categories = models.ManyToManyField(Category, through=PostCategory,
                                        choices=__categories, null=False)
    title = models.CharField(max_length=255, null=False)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return 'Статья: ' + self.title + ' Автор: ' + self.author.user.username

    class Meta:
        ordering = ('-post_time', )
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) > 124:
            return self.text[:124] + '...'
        else:
            return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now())
    rating = models.IntegerField(default=0)

    def __str__(self):
        return 'Пост: ' + self.post.title + ' Автор: ' + self.user.username

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Comment or Post, on_delete=models.CASCADE)
