import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestPostAPI:
    """Тесты для API постов."""

    def test_get_posts_list(self, api_client, post):
        """Тест получения списка постов."""
        url = reverse('api:post-list')
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert 'results' in response.data
        assert len(response.data['results']) == 1

    def test_get_post_detail(self, api_client, post):
        """Тест получения поста по ID."""
        url = reverse('api:post-detail', kwargs={'pk': post.pk})
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert response.data['text'] == post.text
        assert response.data['author'] == post.author.username

    def test_create_post_authenticated(self, api_client, user_token, group):
        """Тест создания поста авторизованным пользователем."""
        url = reverse('api:post-list')
        data = {
            'text': 'Новый тестовый пост',
            'group': group.pk
        }
        
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = api_client.post(url, data)
        
        assert response.status_code == 201
        assert response.data['text'] == data['text']

    def test_create_post_unauthenticated(self, api_client):
        """Тест создания поста неавторизованным пользователем."""
        url = reverse('api:post-list')
        data = {'text': 'Новый пост'}
        
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_update_own_post(self, api_client, user_token, post):
        """Тест обновления своего поста."""
        url = reverse('api:post-detail', kwargs={'pk': post.pk})
        data = {'text': 'Обновленный текст'}
        
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = api_client.patch(url, data)
        
        assert response.status_code == 200
        assert response.data['text'] == data['text']

    def test_update_foreign_post(self, api_client, another_user_token, post):
        """Тест обновления чужого поста."""
        url = reverse('api:post-detail', kwargs={'pk': post.pk})
        data = {'text': 'Попытка обновить чужой пост'}
        
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + another_user_token)
        response = api_client.patch(url, data)
        
        assert response.status_code == 403

    def test_delete_own_post(self, api_client, user_token, post):
        """Тест удаления своего поста."""
        url = reverse('api:post-detail', kwargs={'pk': post.pk})
        
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = api_client.delete(url)
        
        assert response.status_code == 204

    def test_delete_foreign_post(self, api_client, another_user_token, post):
        """Тест удаления чужого поста."""
        url = reverse('api:post-detail', kwargs={'pk': post.pk})
        
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + another_user_token)
        response = api_client.delete(url)
        
        assert response.status_code == 403
