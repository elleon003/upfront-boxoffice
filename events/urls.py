from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.event_list, name='event_list'),
    path(
        '<slug:event>/<int:year>/<int:month>/<int:day>',
        views.event_detail,
        name='event_detail'
    ),
]
