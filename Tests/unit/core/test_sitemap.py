import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_sitemap_exists(client):
    response = client.get('/sitemap.xml')
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/xml'

@pytest.mark.django_db
def test_robots_txt_exists(client):
    response = client.get('/robots.txt')
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/plain'
