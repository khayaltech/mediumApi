from django.contrib import admin

from .models import Article, ArticleViews, Tag


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["pkid", "author", "slug", "article_read_time", "views"]
    list_display_links = ["pkid", "author"]
    prepopulated_fields = {
        "slug": ("title",),
    }


class TagAdmin(admin.ModelAdmin):
    list_display = [
        "tag",
    ]
    prepopulated_fields = {
        "slug": ("tag",),
    }


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ArticleViews)
