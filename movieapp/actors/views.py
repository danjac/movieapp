# Django
from django.template.response import TemplateResponse

# MovieApp
from movieapp.movies import tmdb_api
from movieapp.movies.formatters import format_people, format_person


def actor_list(request):
    try:
        page = int(request.GET["page"])
    except (KeyError, ValueError):
        page = 1

    actors = tmdb_api.popular_people(page)
    return TemplateResponse(
        request, "actors/index.html", {"actors": format_people(actors)}
    )


def actor_detail(request, actor_id):

    actor = tmdb_api.person(actor_id)
    social = tmdb_api.links(actor_id)
    credits = tmdb_api.credits(actor_id)

    return TemplateResponse(
        request,
        "actors/detail.html",
        {"actor": format_person(actor), "social": social, "credits": credits},
    )
