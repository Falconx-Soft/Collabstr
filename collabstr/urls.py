import imp
import site
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from user.sitemaps import StaticViewSitemap

from user.sitemaps2 import PostSitemap


sitemaps2={
    'posts':PostSitemap
}

sitemaps = {
    'static': StaticViewSitemap,
    'posts':PostSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml',sitemap, {'sitemaps':sitemaps,}, name='django.contrib.sitemaps.views.sitemap'),
    path(
        'sitemap2.xml',sitemap, {'sitemaps':sitemaps2}, name='django.contrib.sitemaps.views.sitemap'
    ),
    path('accounts/', include('allauth.urls')),
    path('', include('user.urls')),
    path('', include('chat.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
