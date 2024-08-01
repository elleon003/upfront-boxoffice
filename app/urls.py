from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from events.sitemaps import EventSitemap

sitemaps = {
    'events': EventSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('events/', include('events.urls', namespace='events')),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    )
]
