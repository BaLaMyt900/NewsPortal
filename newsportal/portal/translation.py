from .models import Category, Post, Comment
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ('name',)


@register(Post)
class PostTranslation(TranslationOptions):
    fields = ('title', 'text', )


@register(Comment)
class CommentTranslation(TranslationOptions):
    fields = ('text', )