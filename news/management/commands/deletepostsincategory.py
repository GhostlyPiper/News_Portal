from django.core.management.base import BaseCommand
from news.models import Post, Category


class Command(BaseCommand):
    # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    help = 'Удаляет посты из указанных категорий'
    # Напоминает ли о миграциях. Если True — то будет напоминание о том,
    # что не сделаны все миграции (если такие есть)
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('cats2delete', nargs='+', type=str)

    def handle(self, *args, **options):

        for cat_id in options['cats2delete']:

            # спрашиваем пользователя действительно ли он хочет удалить
            # все посты из заданной категории
            self.stdout.write(
                'Удалить все посты в категории "%s"? yes/no' % cat_id)
            answer = input()  # считываем подтверждение

            if answer.lower() == 'no':
                self.stdout.write(self.style.ERROR(
                    'Удаление отменено!'))

            # в случае подтверждения действительно удаляем все посты
            if answer.lower() == 'yes':

                try:
                    category = Category.objects.get(name=cat_id)
                    Post.objects.filter(postCategory=category).delete()
                    self.stdout.write(self.style.SUCCESS(
                        'Успешно удалены посты в категории "%s"' % cat_id))
                # Если такой категории не существует выводим об этом сообщение
                except Category.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f'Категории "{cat_id}" не существует!'))

            # в случае неправильного подтверждения,
            # говорим что в доступе отказано
            if answer.lower() != 'yes' and answer.lower() != 'no':
                self.stdout.write(self.style.ERROR(
                    'Введён некорректный ответ, в доступе отказано!'))
