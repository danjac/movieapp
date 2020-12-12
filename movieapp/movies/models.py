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

        movie.release_date = (
            parser.parse(movie.release_date) if movie.release_date else None
        )
        movie.vote_average = f"{int(round(movie.vote_average * 10))}%"
        return movie


class MovieDetailViewModel(BaseMovieViewModel):
    def __init__(self, movie):
        self.movie = self.movie_model(movie)
        self.movie.genres = ", ".join(genre.name for genre in self.movie.genres)
        self.movie.crew = self.movie.credits.crew[:2]
        self.movie.cast = [
            self.cast_model(cast) for cast in self.movie.credits.cast[:5]
        ]
        self.movie.images = [
            self.image_model(image) for image in self.movie.images.backdrops[:9]
        ]
        if self.movie.videos.results:
            self.movie.trailer = self.movie.videos.results[0].key
        else:
            self.movie.trailer = None

    def image_model(self, image):
        image.original = f"https://image.tmdb.org/t/p/original/{image['file_path']}"
        image.thumbnail = f"https://image.tmdb.org/t/p/w500/{image['file_path']}"
        return image

    def cast_model(self, cast):
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
        self.popular_movies = self.movie_models(popular_movies)
        self.now_playing = self.movie_models(now_playing)

    def movie_models(self, movies):
        return [self.movie_model(movie) for movie in movies]

    def movie_model(self, movie):
        movie = super().movie_model(movie)

        movie.genres = ", ".join(
            [
                self.genres[genre_id]
                for genre_id in movie.genre_ids
                if genre_id in self.genres
            ]
        )

        return movie

    def as_dict(self):
        return {"popular_movies": self.popular_movies, "now_playing": self.now_playing}
