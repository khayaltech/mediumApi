from django.urls import path

from .views import (
    followunfollowView,
    getFollowerView,
    profilDetailView,
    profileListView,
    profileUpdateView,
)

urlpatterns = [
    path("all/", profileListView, name="all-profiles"),
    path("<str:username>/", profilDetailView, name="profile-detail"),
    path("update/<str:username>/", profileUpdateView, name="profile-update"),
    path("followers/<str:username>/", getFollowerView, name="followers"),
    path("<str:username>/follow/", followunfollowView, name="follow-unfollow"),
]
