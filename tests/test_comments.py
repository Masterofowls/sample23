import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestCommentAPI:
    """Тесты для API комментариев."""

    def test_get_comments_list(self, api_client, post, comment):
        """Тест получения списка комментариев к посту."""
        url = reverse('api:comment-list', kwargs={'post_id': post.pk})
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert 'results' in response.data
        assert len(response.data['results']) == 1

    def test_create_comment_authenticated(self, api_client, user_token, post):
        """Тест создания комментария авторизованным пользователем."""
        url = reverse('api:comment-list', kwargs={'post_id': post.pk})
        data = {'text': 'Новый комментарий'}
        
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = api_client.post(url, data)
        
        assert response.status_code == 201
        assert response.data['text'] == data['text']

    def test_create_comment_unauthenticated(self, api_client, post):
        """Тест создания комментария неавторизованным пользователем."""
        url = reverse('api:comment-list', kwargs={'post_id': post.pk})
        data = {'text': 'Новый комментарий'}
        
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_update_own_comment(self, api_client, user_token, post, comment):
        """Тест обновления своего комментария."""
        url = reverse('api:comment-detail', kwargs={
            'post_id': post.pk,
            'pk': comment.pk
        })
        data = {'text': 'Обновленный комментарий'}
        
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = api_client.patch(url, data)
        
        assert response.status_code == 200
        assert response.data['text'] == data['text']

    def test_update_foreign_comment(self, api_client, another_user_token, post, comment):
        """Тест обновления чужого комментария."""
        url = reverse('api:comment-detail', kwargs={
            'post_id': post.pk,
            'pk': comment.pk
        })
        data = {'text': 'Попытка обновить чужой комментарий'}
        
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + another_user_token)
        response = api_client.patch(url, data)
        
        assert response.status_code == 403

    def test_delete_own_comment(self, api_client, user_token, post, comment):
        """Тест удаления своего комментария."""
        url = reverse('api:comment-detail', kwargs={
            'post_id': post.pk,
            'pk': comment.pk
        })
        
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = api_client.delete(url)
        
        assert response.status_code == 204

    def test_delete_foreign_comment(self, api_client, another_user_token, post, comment):
        """Тест удаления чужого комментария."""
        url = reverse('api:comment-detail', kwargs={
            'post_id': post.pk,
            'pk': comment.pk
        })
        
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + another_user_token)
        response = api_client.delete(url)
        
        assert response.status_code == 403
