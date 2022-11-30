from django.urls import path

from .views import createRatingView

urlpatterns = [path("<str:article_id>/", createRatingView, name="rate-article")]
