from django.urls import path

from .views import (
    articleCreateView,
    articleDeleteView,
    articleDetailView,
    articleListView,
    articleUpdateView,
)

urlpatterns = [
    path("all/", articleListView, name="all-articles"),
    path("create/", articleCreateView, name="create-article"),
    path("details/<slug:slug>/", articleDetailView, name="article-detail"),
    path("update/<slug:slug>/", articleUpdateView, name="article-update"),
    path("delete/<slug:slug>/", articleDeleteView, name="delete-article"),
]
