from django.urls import path

from .views import voteApiView

urlpatterns = [path("<slug:slug>/", voteApiView, name="user-reaction")]
