import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestGroupAPI:
    """Тесты для API групп."""

    def test_get_groups_list(self, api_client, group):
        """Тест получения списка групп."""
        url = reverse('api:group-list')
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert 'results' in response.data
        assert len(response.data['results']) == 1

    def test_get_group_detail(self, api_client, group):
        """Тест получения группы по ID."""
        url = reverse('api:group-detail', kwargs={'pk': group.pk})
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert response.data['title'] == group.title
        assert response.data['slug'] == group.slug
        assert response.data['description'] == group.description
