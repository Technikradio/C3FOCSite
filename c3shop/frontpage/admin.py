from django.contrib import admin
from .models import Profile, Media, Article, ArticleMedia, ArticleRequested
# Register your models here.
admin.site.register(Profile)
admin.site.register(Media)
admin.site.register(ArticleRequested)
admin.site.register(Article)
admin.site.register(ArticleMedia)

