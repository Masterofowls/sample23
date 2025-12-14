"""
Management команда для подготовки тестовых данных.
Аналог bash-скрипта set_up_data.sh для Windows.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from posts.models import Comment, Group, Post

User = get_user_model()


class Command(BaseCommand):
    help = 'Подготовка тестовых данных для API Yatube'

    def handle(self, *args, **options):
        self.stdout.write('Очистка базы данных...')
        
        # Удаляем все данные
        Comment.objects.all().delete()
        Post.objects.all().delete()
        Group.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        self.stdout.write(self.style.SUCCESS('База данных очищена'))
        
        # Создаем тестовых пользователей
        self.stdout.write('Создание пользователей...')
        
        # Создаем суперпользователя (если его нет)
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin'
            )
        
        # Создаем тестовых пользователей
        user1 = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        
        user2 = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='authorpass123'
        )
        
        self.stdout.write(self.style.SUCCESS(
            f'Созданы пользователи: {user1.username}, {user2.username}'
        ))
        
        # Создаем группы
        self.stdout.write('Создание групп...')
        
        group1 = Group.objects.create(
            title='Тестовая группа',
            slug='test',
            description='Это тестовая группа для проверки API'
        )
        
        group2 = Group.objects.create(
            title='Математика',
            slug='math',
            description='Посты на тему математики'
        )
        
        group3 = Group.objects.create(
            title='Программирование',
            slug='coding',
            description='Посты о программировании и разработке'
        )
        
        self.stdout.write(self.style.SUCCESS(
            f'Созданы группы: {group1.title}, {group2.title}, {group3.title}'
        ))
        
        # Создаем посты
        self.stdout.write('Создание постов...')
        
        post1 = Post.objects.create(
            text='Первый тестовый пост от testuser',
            author=user1,
            group=group1
        )
        
        post2 = Post.objects.create(
            text='Второй тестовый пост от author',
            author=user2,
            group=group2
        )
        
        post3 = Post.objects.create(
            text='Пост о Python от testuser',
            author=user1,
            group=group3
        )
        
        post4 = Post.objects.create(
            text='Пост о Django от author',
            author=user2,
            group=group3
        )
        
        post5 = Post.objects.create(
            text='Пост без группы от testuser',
            author=user1
        )
        
        self.stdout.write(self.style.SUCCESS(f'Создано постов: 5'))
        
        # Создаем комментарии
        self.stdout.write('Создание комментариев...')
        
        Comment.objects.create(
            author=user2,
            post=post1,
            text='Отличный пост!'
        )
        
        Comment.objects.create(
            author=user1,
            post=post2,
            text='Спасибо за информацию'
        )
        
        Comment.objects.create(
            author=user2,
            post=post3,
            text='Python - лучший язык!'
        )
        
        Comment.objects.create(
            author=user1,
            post=post3,
            text='Согласен полностью'
        )
        
        self.stdout.write(self.style.SUCCESS(f'Создано комментариев: 4'))
        
        self.stdout.write(
            self.style.SUCCESS('\n=== Тестовые данные успешно созданы ===')
        )
        self.stdout.write('\nДанные для входа:')
        self.stdout.write(f'  Администратор: admin / admin')
        self.stdout.write(f'  Пользователь 1: testuser / testpass123')
        self.stdout.write(f'  Пользователь 2: author / authorpass123')
