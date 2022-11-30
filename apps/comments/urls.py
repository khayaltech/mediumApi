from django.urls import path

from .views import commentApiView, commentUpdateDeleteView

urlpatterns = [
    path("<slug:slug>/comment/", commentApiView, name="comments"),
    path(
        "<slug:slug>/comment/<str:id>/",
        commentUpdateDeleteView,
        name="comment",
    ),
]
