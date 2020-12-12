# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse

# Third Party Libraries
import pytest

# MovieApp
from movieapp.users.factories import UserFactory


@pytest.fixture
def get_response():
    return lambda req: HttpResponse()


@pytest.fixture
def user_model():
    return get_user_model()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def anonymous_user():
    return AnonymousUser()


@pytest.fixture
def login_user(client):
    password = "t3SzTP4sZ"
    user = UserFactory()
    user.set_password(password)
    user.save()
    client.login(username=user.username, password=password)
    return user


@pytest.fixture
def movie():
    return {
        "id": 1,
        "genre_ids": [1, 2],
        "title": "Star Wars: A New Hope",
        "poster_path": "/star-wars-a-new-hope.jpg",
        "release_date": "1977-5-4",
        "vote_average": 9,
    }


@pytest.fixture
def genres():
    return [
        {"id": 1, "name": "Drama"},
        {"id": 2, "name": "Sci-fi"},
    ]
