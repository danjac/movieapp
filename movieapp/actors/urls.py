# Django
from django.urls import path

# Local
from . import views

app_name = "actors"


urlpatterns = [
    path("", views.actor_list, name="actor_list"),
    path("<int:actor_id>/", views.actor_detail, name="actor_detail"),
]
