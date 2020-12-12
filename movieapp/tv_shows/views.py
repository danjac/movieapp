# Django
from django.template.response import TemplateResponse

# MovieApp
from movieapp.common import tmdb_api

# Local
from .models import ShowDetailViewModel, ShowListViewModel


def show_list(request):
    view_model = ShowListViewModel(
        popular_shows=tmdb_api.popular_tv(),
        top_rated_shows=tmdb_api.top_rated_tv(),
        genres=tmdb_api.tv_genres(),
    )
    return TemplateResponse(request, "tv_shows/index.html", view_model.as_dict())


def show_detail(request, show_id):
    view_model = ShowDetailViewModel(
        show=tmdb_api.tv_show(show_id), genres=tmdb_api.tv_genres()
    )
    return TemplateResponse(request, "tv_shows/detail.html", view_model.as_dict())
