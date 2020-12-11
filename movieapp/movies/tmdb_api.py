# Django
from django.conf import settings

# Third Party Libraries
import requests

BASE_URL = "https://api.themoviedb.org/3/"


def _fetch_json(url):
    return requests.get(
        BASE_URL + url, headers={"Authorization": f"Bearer {settings.TMDB_API_TOKEN}"},
    ).json()


def popular_movies():
    return _fetch_json("movie/popular")["results"]


def now_playing():
    return _fetch_json("movie/now_playing")["results"]


def movie_genres():
    return _fetch_json("genre/movie/list")["genres"]


def movie(movie_id):
    return _fetch_json(f"movie/{movie_id}?append_to_response=credits,videos,images")


def popular_tv():
    return _fetch_json("tv/popular")["results"]


def top_rated_tv():
    return _fetch_json("tv/top_rated")["results"]


def tv_genres():
    return _fetch_json("genre/tv/list")["results"]


def person(person_id):
    return _fetch_json(f"person/{person_id}")


def links(person_id):
    return _fetch_json(f"person/{person_id}/external_ids")


def credits(person_id):
    return _fetch_json(f"person/{person_id}/credits")
