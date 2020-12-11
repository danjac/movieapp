# Standard Library
import datetime


def get_genre_dict(genres):
    return {g["id"]: g["name"] for g in genres}


def format_movies(movies, genre_dict):
    return [format_movie(movie, genre_dict) for movie in movies]


def format_movie(movie, genre_dict=None):
    dct = {
        **movie,
        "vote_average": f"{movie['vote_average'] * 10}%",
        "release_date": datetime.datetime.strptime(movie["release_date"], "%Y-%m-%d"),
        "poster_path": f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"
        if "poster_path" in movie
        else "https://via.placeholder.com/500x750",
    }

    if genre_dict is not None and "genre_ids" in movie:
        movie["genres "] = ", ".join(
            [genre_dict[genre_id] for genre_id in movie.get("genre_ids", [])]
        )

    return dct


def format_movie_detail(movie):
    dct = {
        **format_movie(movie),
        "genres": ", ".join([g["name"] for g in movie["genres"]]),
    }
    if "credits" in movie:
        dct |= {
            "crew": movie["credits"]["crew"][:2],
            "cast": format_people(movie["credits"]["cast"][:5]),
        }

    if "images" in movie:
        dct |= {"images": format_images(movie["images"]["backdrops"])[:9]}

    return dct


def format_images(images):
    return [
        {
            "original": f"https://image.tmdb.org/t/p/original/{image['file_path']}",
            "thumbnail": f"https://image.tmdb.org/t/p/w500/{image['file_path']}",
        }
        for image in images
    ]


def format_person(person):
    known_for = ", ".join(
        [
            item["title"] if item["media_type"] == "movie" else item["name"]
            for item in person.get("known_for", [])
        ]
    )

    return {
        **person,
        "known_for": known_for,
        "profile_path": f"https://image.tmdb.org/t/p/w300{person['profile_path']}"
        if "profile_path" in person
        else f"https://ui-avatars.com/api/?size=235&name={person['name']}",
    }


def format_people(people):
    return [format_person(person) for person in people]
