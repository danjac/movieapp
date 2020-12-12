# Third Party Libraries
from box import Box
from dateutil import parser


class BaseMovieViewModel:
    def movie_model(self, movie):
        movie = Box(movie, default_box=True)
        movie.poster_path = (
            f"https://image.tmdb.org/t/p/w500/{movie.poster_path}"
            if movie.poster_path
            else "https://via.placeholder.com/500x750"
        )

        movie.release_date = parser.parse(movie.release_date)
        movie.vote_average = f"{int(movie.vote_average * 10)}%"
        return movie


class MovieDetailViewModel(BaseMovieViewModel):
    def __init__(self, movie):
        self.movie = self.movie_model(movie)
        self.movie.genres = ", ".join(genre.name for genre in self.movie.genres)
        self.movie.crew = self.movie.credits.crew[:2]
        self.movie.cast = [
            self.format_cast(cast) for cast in self.movie.credits.cast[:5]
        ]
        self.movie.images = [
            self.format_image(image) for image in self.movie.images.backdrops[:9]
        ]

    def format_image(self, image):
        image.original = f"https://image.tmdb.org/t/p/original/{image['file_path']}"
        image.thumbnail = f"https://image.tmdb.org/t/p/w500/{image['file_path']}"
        return image

    def format_cast(self, cast):
        cast.profile_path = (
            f"https://image.tmdb.org/t/p/w300{cast.profile_path}"
            if cast.profile_path
            else "https://via.placeholder.com/300x450"
        )
        return cast

    def as_dict(self):
        return {"movie": self.movie}


class MovieListViewModel(BaseMovieViewModel):
    def __init__(self, popular_movies, now_playing, genres):
        self.genres = {genre["id"]: genre["name"] for genre in genres}
        self.popular_movies = self.format_movies(popular_movies)
        self.now_playing = self.format_movies(now_playing)

    def format_movies(self, movies):
        return [self.format_movie(movie) for movie in movies]

    def format_movie(self, movie):
        movie = self.movie_model(movie)

        movie.genres = ", ".join(
            [self.genres[genre_id] for genre_id in movie.genre_ids]
        )

        return movie

    def as_dict(self):
        return {"popular_movies": self.popular_movies, "now_playing": self.now_playing}
