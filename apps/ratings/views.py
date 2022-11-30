from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.articles.models import Article

from .exceptions import AlreadyRated, CantRateYourArticle
from .models import Rating
from .serializers import RatingSerializer


class CreateArticleRatingApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RatingSerializer

    @swagger_auto_schema(request_body=RatingSerializer)
    def post(self, request, article_id):
        data = request.data
        article = Article.objects.get(id=article_id)
        author = request.user
        if article.author == author:
            raise CantRateYourArticle
        already_exists = article.article_ratings.filter(
            rated_by__pkid=author.pkid
        ).exists()
        if already_exists:
            raise AlreadyRated
        elif data["value"] == 0:
            formatted_response = {"detail": "You can't give a zero rating"}
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            rating = Rating.objects.create(
                article=article,
                rated_by=request.user,
                value=data["value"],
            )

            return Response(
                {"success": "Rating has been added"}, status=status.HTTP_201_CREATED
            )


createRatingView = CreateArticleRatingApiView.as_view()
