from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.articles.models import Article
from apps.common.models import TimeStampedUUIDModel

from .managers import ReactionManager

User = get_user_model()


# Create your models here.
class Reaction(TimeStampedUUIDModel):
    class Reactions(models.IntegerChoices):
        LIKE = 1, _("like")
        DISLIKE = -1, _("dislike")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_reactions"
    )
    reaction = models.IntegerField(
        verbose_name=_("like-dislike"), choices=Reactions.choices
    )

    objects = ReactionManager()

    class Meta:
        unique_together = ["user", "article", "reaction"]

    def __str__(self):
        return (
            f"{self.user.username} voted on {self.article.title} with a {self.reaction}"
        )
