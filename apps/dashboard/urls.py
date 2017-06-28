from django.conf.urls import url
from . import views
app_name='dashboard'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new$', views.add_user, name='add_user'),
    url(r'^create$', views.create_user, name='create_user'),
    url(r'^edit/(?P<user_id>\d+)/$', views.edit_user, name='edit_user'),
    url(r'^update/(?P<user_id>\d+)/$', views.update_user, name='update_user'),
    url(r'^destroy_user/(?P<user_id>\d+)$', views.destroy_user, name='destroy_user'),
    url(r'^show/(?P<user_id>\d+)$', views.show_user, name='show_user'),
    url(r'^create_message/(?P<wall_id>\d+)$', views.create_message, name='create_message'),
    url(r'^create_comment/(?P<message_id>\d+)$', views.create_comment, name='create_comment'),
]