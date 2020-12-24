# Django
from django.template.response import TemplateResponse

# MovieApp
from movieapp.common import tmdb_api

# Local
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


def search_movies(request):
    search = request.GET.get("search")
    if search and len(search) > 2:
        results = tmdb_api.search_movies(search)[:7]
    else:
        results = []

    return TemplateResponse(
        request, "movies/search/_results.html", {"results": results, "search": search},
    )
