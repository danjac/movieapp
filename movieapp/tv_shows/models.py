# Django
from django.urls import reverse

# Third Party Libraries
from box import Box
from dateutil import parser


class BaseShowModel:
    def __init__(self, genres):
        self.genres = {g["id"]: g["name"] for g in genres}

    def show_model(self, show):
        show = Box(show, default_box=True)
        show.poster_path = (
            f"https://image.tmdb.org/t/p/w500/{show.poster_path}"
            if show.poster_path
            else "https://via.placeholder.com/500x750"
        )
        show.vote_average = f"{int(round(show.vote_average * 10))}%"
        show.first_air_date = parser.parse(show.first_air_date)
        show.genres = show.genres = ", ".join(
            [
                self.genres[genre_id]
                for genre_id in show.genre_ids
                if genre_id in self.genres
            ]
        )

        return show


class ShowListViewModel(BaseShowModel):
    def __init__(self, popular_shows, top_rated_shows, genres):
        super().__init__(genres)
        self.popular_shows = [self.show_model(show) for show in popular_shows]
        self.top_rated_shows = [self.show_model(show) for show in top_rated_shows]

    def show_model(self, show):
        show = super().show_model(show)
        show.url = reverse("tv_shows:show_detail", args=[show.id])
        return show

    def as_dict(self):
        return {
            "top_rated_shows": self.top_rated_shows,
            "popular_shows": self.popular_shows,
        }


class ShowDetailViewModel(BaseShowModel):
    def __init__(self, show, genres):
        super().__init__(genres)
        self.show = self.show_model(show)
        self.show.cast = [self.cast_model(cast) for cast in self.show.credits.cast[:5]]
        self.show.images = [
            self.image_model(image) for image in self.show.images.backdrops[:9]
        ]

        if self.show.videos.results:
            self.show.trailer = self.show.videos.results[0].key
        else:
            self.show.trailer = None

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
        return {"show": self.show}
