from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index$', views.harttv_index, name='harttv_index'),
    url(r'^show/(?P<show_maze_id>\d+)$', views.view_show, name='view_show'),
    url(r'^sheriffsrsdelete$', views.delete_all_shows, name='delete_all_shows'),
]
