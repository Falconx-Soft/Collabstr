from django.contrib.sitemaps import Sitemap
from .models import JoinInfluencer

class PostSitemap(Sitemap):
    def items(self):
        return JoinInfluencer.objects.all()