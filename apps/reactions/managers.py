from django.contrib.auth import get_user_model
from django.db import models


class ReactionManager(models.Manager):
    def likes(self):
        return self.get_queryset().filter(reaction__gt=0).count()

    def dislikes(self):
        return self.get_queryset().filter(reaction__lt=0).count()

    def has_reacted(self):
        request = self.context.get("request")
        if request:
            self.get_queryset().filter(user=request)
