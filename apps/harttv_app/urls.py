from django.conf.urls import url
from . import views
app_name='harttv'
urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^show/(?P<show_maze_id>\d+)$', views.view_show, name='view_show'),
    url(r'^sheriffsrsdelete$', views.delete_all_shows, name='delete_all_shows'),
    url(r'^show/search$', views.test_search_bar, name='test_search_bar'),
    url(r'^show/search/results$', views.search_results, name='search_results'),
    url(r'^show/(?P<show_id>\d+)/handle_add_review$', views.handle_add_review, name='handle_add_review'),
]
