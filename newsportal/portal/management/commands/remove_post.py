from django.core.management import BaseCommand
from portal.models import Post, Category


class Command(BaseCommand):
    help = 'Удаление всех постов с переданной категорией'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.write(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')
        answer = input()

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(categories=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Успешно удалены все посты с категорией {category.name}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Невозможно найти категорию {category.name}'))
