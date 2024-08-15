from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from events.sitemaps import EventSitemap
from . import views

sitemaps = {
    'events': EventSitemap,
}

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('account/', include('account.urls')),
    path('events/', include('events.urls', namespace='events')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path('__reload__/', include("django_browser_reload.urls")),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    
