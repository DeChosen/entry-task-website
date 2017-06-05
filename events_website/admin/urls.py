from django.conf.urls import patterns, url
import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [url(r'^home/$', views.redirect_page),
               url(r'^home/(?P<page_num>\d+)/$$', views.home_page),
               url(r'^home/event(?P<event_id>\d+)/$', views.show_event, name='show event'),
               url(r'^home/event(?P<event_id>\d+)/upload_photo/$', views.submit_photo, name='submit photo'),
               url(r'^session_expired/$', views.session_expired),
               url(r'^home/addevent/', views.addevent, name= 'add event'),
               url(r'^home/event(?P<event_id>\d+)/addtag/', views.addtag, name='add tag')]

