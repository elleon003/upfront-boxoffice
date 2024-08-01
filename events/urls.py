from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.event_list, name='event_list'),
    # path('', views.EventListView.as_view(), name='event_list'),
    path(
        '<slug:event>/<int:year>/<int:month>/<int:day>',
        views.event_detail,
        name='event_detail'
    ),
    path('<int:event_id>/share/', views.event_share, name='event_share'),
    path( 'tag/<slug:tag_slug>/', views.event_list, name='event_list_by_tag'),
    path('search/', views.event_search, name='event_search' )

]   
