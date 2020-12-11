# Django
from django.template.response import TemplateResponse

# Local
from . import tmdb_api
from .utils import format_movie_detail, format_movies, get_genre_dict


def movie_list(request):
    genre_dict = get_genre_dict(tmdb_api.movie_genres())
    popular_movies = format_movies(tmdb_api.popular_movies(), genre_dict)
    now_playing = format_movies(tmdb_api.now_playing(), genre_dict)

    return TemplateResponse(
        request,
        "movies/index.html",
        {"popular_movies": popular_movies, "now_playing": now_playing,},
    )


def movie_detail(request, movie_id):
    movie = format_movie_detail(tmdb_api.movie(movie_id))
    return TemplateResponse(request, "movies/detail.html", {"movie": movie})
