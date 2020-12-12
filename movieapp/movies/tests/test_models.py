# Local
from ..models import MovieListViewModel


class TestMovieListViewModel:
    def test_model(self, movie, genres):
        view_model = MovieListViewModel(
            popular_movies=[movie], now_playing=[movie], genres=genres
        )

        assert view_model.popular_movies[0].vote_average == "90%"
        assert view_model.popular_movies[0].release_date.year == 1977
        assert view_model.popular_movies[0].genres == "Drama, Sci-fi"
