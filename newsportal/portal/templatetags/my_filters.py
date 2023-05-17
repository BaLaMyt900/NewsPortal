from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def censor(text: str):
    bad_words = ['редиска']
    for word in text.split():
        if word.lower() in bad_words:
            text = text.replace(word, word[:1] + '*' * (len(word)-1), 1)

    return text

@register.filter
def get_list(list, value):
    return list.getlist(value)

