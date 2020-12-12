# Django
from django.urls import path

# Local
from . import views

app_name = "movies"


urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("search/", views.search_movies, name="search_movies"),
    path("<int:movie_id>/", views.movie_detail, name="movie_detail"),
]
