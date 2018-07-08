from hello.models import User, Page

from rest_framework.test import APIClient
import pytest


def create_user(email, is_admin=False):
    return User.objects.create(email=email, is_admin=is_admin)


def create_page(user, title):
    return Page.objects.create(user=user, title=title)


@pytest.mark.django_db
def test_real_page_no_auth():
    client = APIClient()
    response = client.get('/api/real-pages')

    assert response.status_code == 401


@pytest.mark.django_db
def test_real_page_is_admin():
    client = APIClient()
    admin_user = create_user('a@a.pl', is_admin=True)
    page_user = create_user('b@b.pl')
    page = create_page(page_user, 'foo')

    client.force_login(admin_user)
    response = client.patch(
        f'/api/real-pages/{page.id}',
        {'title': 'foobar'})

    assert response.status_code == 200
    assert response.data == {
        'id': page.id,
        'user': page_user.id,
        'title': 'foobar',
        'description': '',
    }


@pytest.mark.django_db
def test_real_page_is_owner():
    client = APIClient()
    page_user = create_user('b@b.pl')
    page = create_page(page_user, 'foo')

    client.force_login(page_user)
    response = client.patch(
        f'/api/real-pages/{page.id}',
        {'title': 'foobar'})

    assert response.status_code == 200
    assert response.data == {
        'id': page.id,
        'user': page_user.id,
        'title': 'foobar',
        'description': '',
    }
