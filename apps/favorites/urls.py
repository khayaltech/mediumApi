from django.urls import path

from .views import addToFavoritesView, userFavoritesView

urlpatterns = [
    path("articles/me/", userFavoritesView, name="my-favorites"),
    path("<slug:slug>/", addToFavoritesView, name="favorite-article"),
]
