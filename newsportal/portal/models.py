import django.utils.timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from django.core.cache import cache


class PortalUser(AbstractUser):
    """ Модель пользователя портала. """
    rating = models.IntegerField(default=0)
    post_active = models.ManyToManyField("Post", through="PostActivity")
    comment_active = models.ManyToManyField("Comment", through="CommentActivity")

    def __str__(self):
        return self.username

    def update_rating(self):
        comments_rating = Comment.objects.filter(user=self).aggregate(Sum('rating'))['rating__sum']
        comments_rating = comments_rating if comments_rating else 0
        try:
            if_author = Author.objects.get(user=self)
        except Author.DoesNotExist:
            self.rating = comments_rating
        else:
            if_author.update_rating()
            self.rating = comments_rating + if_author.rating
        self.save()


class Author(models.Model):
    """ Модель автора портала. Создается с привязкой к пользователю """
    user = models.OneToOneField(PortalUser, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    numbers_of_posts = models.IntegerField(default=3)

    def __str__(self):
        return self.user.username

    @property
    def post_count(self):
        return len(Post.objects.filter(author=self))

    def new_post(self):
        self.numbers_of_posts -= 1
        self.save()

    def update_numbers_of_posts(self):
        self.numbers_of_posts = 3
        self.save()

    def update_rating(self):
        posts = Post.objects.filter(author=self)
        try:
            posts_rating = posts.aggregate(Sum('rating'))['rating__sum'] * 3
        except TypeError:
            posts_rating = 0
        try:
            posts_comments_rating = sum(
                [Comment.objects.filter(post__in=posts).aggregate(Sum('rating'))['rating__sum']])
        except TypeError:
            posts_comments_rating = 0
        self.rating = posts_rating + posts_comments_rating
        self.save()

    class Meta:
        verbose_name = 'Автора'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    """ Категория поста """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    """ Модель поста """
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    __types = [
        ('A', 'Статья'),
        ('N', 'Новость')
    ]
    type = models.CharField(max_length=1, choices=__types)
    post_time = models.DateTimeField(default=django.utils.timezone.now)
    categories = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=255, null=False)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def like(self, user: PortalUser):
        try:
            PostActivity.objects.get(user=user, activity=self)
        except PostActivity.DoesNotExist:
            self.rating += 1
            self.save()
            PostActivity.objects.create(user=user, activity=self)

    def dislike(self, user):
        try:
            PostActivity.objects.get(user=user, activity=self)
        except PostActivity.DoesNotExist:
            self.rating -= 1
            self.save()
            PostActivity.objects.create(user=user, activity=self)

    def preview(self):
        if len(self.text) > 124:
            return self.text[:121] + '...'
        else:
            return self.text

    def mail_preview(self):
        if len(self.text) > 50:
            return self.text[:47] + '...'
        else:
            return self.text

    def edit(self, new):
        self.title = new.title
        self.type = new.type
        self.text = new.text
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        cache.delete(f'post-{self.pk}')

    class Meta:
        ordering = ('-post_time', )
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(PortalUser, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=django.utils.timezone.now)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.text if len(self.text) < 15 else self.text[:12] + '...'

    @property
    def prewiew(self):
        return self.text if len(self.text) < 15 else self.text[:12] + '...'

    def like(self, user):
        try:
            CommentActivity.objects.get(user=user, activity=self)
        except CommentActivity.DoesNotExist:
            self.rating += 1
            self.save()
            PortalUser.objects.get(pk=self.user.pk).update_rating()
            CommentActivity.objects.create(user=user, activity=self)

    def dislike(self, user):
        try:
            CommentActivity.objects.get(user=user, activity=self)
        except CommentActivity.DoesNotExist:
            self.rating -= 1
            self.save()
            CommentActivity.objects.create(user=user, activity=self)

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class PostActivity(models.Model):
    user = models.ForeignKey(PortalUser, on_delete=models.CASCADE)
    activity = models.ForeignKey(Post, on_delete=models.CASCADE)


class CommentActivity(models.Model):
    user = models.ForeignKey(PortalUser, on_delete=models.CASCADE)
    activity = models.ForeignKey(Comment, on_delete=models.CASCADE)


class Subscribers(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(PortalUser, on_delete=models.CASCADE)