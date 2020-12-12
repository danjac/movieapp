This is a rewrite of the Laravel movies example app in the Django stack:

https://github.com/drehimself/laravel-movies-example


## Getting started

You need docker-compose and docker to get started.

Copy the *.env.example* file to *.env* and set the **TMDB_API_TOKEN** .

You can get an API key ![here](https://www.themoviedb.org/documentation/api). Make sure to use the "API Read Access Token (v4 auth)" from the TMDb dashboard.

> docker-compose build

> ./scripts/manage makemigrations users

> ./scripts/manage migrate

> docker-compose up -d

Demo: https://dj-movieapp.herokuapp.com
