from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Recipe

class RecipeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Recipe.objects.filter(public=True)

    def lastmod(self, obj):
        return obj.updated_at

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['recipe_list']

    def location(self, item):
        return reverse(item)
