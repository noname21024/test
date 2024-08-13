from django.contrib import sitemaps
from django.urls import reverse
from .models import Mangas

class StaticViewsSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreg = "daily"


    def items(self):
        return [
            'home',
            'security',
            'following-page',
            'login',
            'logout',
            'register',
        ]
    
    def location(self, item):
        return reverse(item)
    
class MangasSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreg = "daily"

    def items(self):
        return Mangas.objects.all()
    
    def location(self, item):
        return "/room/%s" % item.name
    
