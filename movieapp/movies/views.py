# Django
from django.template.response import TemplateResponse

# Local
from . import tmdb_api
from .models import MovieDetailViewModel, MovieListViewModel


def movie_list(request):
    view_model = MovieListViewModel(
        popular_movies=tmdb_api.popular_movies(),
        now_playing=tmdb_api.now_playing(),
        genres=tmdb_api.movie_genres(),
    )
    return TemplateResponse(request, "movies/index.html", view_model.as_dict())


def movie_detail(request, movie_id):
    view_model = MovieDetailViewModel(tmdb_api.movie(movie_id))
    return TemplateResponse(request, "movies/detail.html", view_model.as_dict())
