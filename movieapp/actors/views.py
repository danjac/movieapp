# Django
from django.template.response import TemplateResponse

# MovieApp
from movieapp.common import tmdb_api

# Local
from .models import ActorDetailViewModel, ActorListViewModel


def actor_list(request):
    try:
        page = int(request.GET["page"])
    except (KeyError, ValueError):
        page = 1

    view_model = ActorListViewModel(tmdb_api.popular_people(page))
    return TemplateResponse(request, "actors/index.html", view_model.as_dict())


def actor_detail(request, actor_id):

    view_model = ActorDetailViewModel(
        actor=tmdb_api.person(actor_id),
        social=tmdb_api.links(actor_id),
        credits=tmdb_api.credits(actor_id),
    )

    return TemplateResponse(request, "actors/detail.html", view_model.as_dict())
