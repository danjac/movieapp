# Django
from django.urls import path

# Local
from . import views

app_name = "tv_shows"


urlpatterns = [
    path("", views.show_list, name="show_list"),
    path("<int:show_id>/", views.show_detail, name="show_detail"),
]
