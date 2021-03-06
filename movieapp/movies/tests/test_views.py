# Django
from django.urls import reverse

# MovieApp
from movieapp.common import tmdb_api

# Local
from .. import views


class TestMovieList:
    def test_get(self, rf, movie, genres, mocker):
        mock_popular_movies = mocker.patch.object(tmdb_api, "popular_movies")
        mock_popular_movies.return_value = [movie]

        mock_now_playing = mocker.patch.object(tmdb_api, "now_playing")
        mock_now_playing.return_value = [movie]
        mock_genres = mocker.patch.object(tmdb_api, "movie_genres")

        mock_genres.return_value = genres

        resp = views.movie_list(rf.get(reverse("movies:movie_list")))
        assert resp.status_code == 200
        assert len(resp.context_data["popular_movies"]) == 1
        assert len(resp.context_data["now_playing"]) == 1
