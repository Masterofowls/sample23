import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from posts.models import Comment, Group, Post

User = get_user_model()


@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    return APIClient()


@pytest.fixture
def user(django_user_model):
    """Фикстура для создания пользователя."""
    return django_user_model.objects.create_user(
        username='testuser',
        password='testpass123'
    )


@pytest.fixture
def another_user(django_user_model):
    """Фикстура для создания второго пользователя."""
    return django_user_model.objects.create_user(
        username='anotheruser',
        password='anotherpass123'
    )


@pytest.fixture
def user_token(user):
    """Фикстура для создания токена пользователя."""
    token, _ = Token.objects.get_or_create(user=user)
    return token.key


@pytest.fixture
def another_user_token(another_user):
    """Фикстура для создания токена другого пользователя."""
    token, _ = Token.objects.get_or_create(user=another_user)
    return token.key


@pytest.fixture
def group():
    """Фикстура для создания группы."""
    return Group.objects.create(
        title='Тестовая группа',
        slug='test',
        description='Описание тестовой группы'
    )


@pytest.fixture
def post(user, group):
    """Фикстура для создания поста."""
    return Post.objects.create(
        text='Тестовый пост',
        author=user,
        group=group
    )


@pytest.fixture
def comment(user, post):
    """Фикстура для создания комментария."""
    return Comment.objects.create(
        author=user,
        post=post,
        text='Тестовый комментарий'
    )
