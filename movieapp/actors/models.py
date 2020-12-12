# Standard Library
import datetime
import operator

# Django
from django.urls import reverse

# Third Party Libraries
from box import Box
from dateutil import parser, relativedelta


class ActorDetailViewModel:
    def __init__(self, actor, social, credits):
        self.actor = self.actor_model(actor)
        self.social = self.social_model(social)

        cast = Box(credits, default_box=True).cast

        self.known_for_movies = self.known_for_movies_model(cast)
        self.credits = self.credits_model(cast)

    def actor_model(self, actor):
        actor = Box(actor)
        actor.birthday = parser.parse(actor.birthday)
        actor.age = relativedelta.relativedelta(
            datetime.datetime.today(), actor.birthday
        ).years
        actor.profile_path = (
            f"https://image.tmdb.org/t/p/w300/{actor.profile_path}"
            if actor.profile_path
            else "https://via.placeholder.com/300x450"
        )
        return actor

    def social_model(self, social):
        social = Box(social, default_box=True)
        social.twitter = (
            f"https://twitter.com/{social.twitter_id}" if social.twitter_id else None
        )
        social.facebook = (
            f"https://facebook.com/{social.facebook_id}" if social.facebook_id else None
        )
        social.instagram = (
            f"https://instagram.com/{social.instagram_id}"
            if social.instagram_id
            else None
        )
        return social

    def known_for_movies_model(self, cast):
        return [self.movie_model(movie) for movie in cast]

    def credits_model(self, cast):
        return sorted(
            [self.credit_model(credit) for credit in cast],
            key=operator.attrgetter("release_date"),
            reverse=True,
        )

    def credit_model(self, credit):
        release_date = credit.release_date or credit.first_release_date
        if release_date:
            release_date = parser.parse(release_date)
        credit.release_date = release_date or datetime.datetime.today()
        credit.release_year = release_date.year if release_date else "Future"
        credit.title = credit.title or credit.name or "Untitled"
        credit.url = reverse("movies:movie_detail", args=[credit.id])
        return credit

    def movie_model(self, movie):
        movie.title = movie.title or movie.name or "Untitled"
        movie.poster_path = (
            f"https://image.tmdb.org/t/p/w185{movie.poster_path}"
            if movie.poster_path
            else "https://via.placeholder.com/185x278"
        )
        # tbd: handle tv credits
        movie.url = reverse("movies:movie_detail", args=[movie.id])
        return movie

    def as_dict(self):
        return {
            "actor": self.actor,
            "social": self.social,
            "known_for_movies": self.known_for_movies,
            "credits": self.credits,
        }


class ActorListViewModel:
    def __init__(self, actors):
        self.actors = [self.actor_model(actor) for actor in actors]

    def actor_model(self, actor):
        actor = Box(actor)
        actor.profile_path = (
            f"https://image.tmdb.org/t/p/w235_and_h235_face{actor.profile_path}"
            if actor.profile_path
            else "https://ui-avatars.com/api/?size=235&name={actor.name}"
        )
        actor.known_for = ", ".join(
            [
                item.title if item.media_type == "movie" else item.name
                for item in actor.known_for
            ]
        )
        return actor

    def as_dict(self):
        return {"actors": self.actors}
