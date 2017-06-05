from django.conf.urls import patterns, url
from views import redirect_home, home_page, display_event, search_event

urlpatterns = patterns('', url(r'^$', redirect_home, name='redirect'),
                       url(r'^(?P<page_num>\d+)/$', home_page, name='home'),
                       url(r'^event(?P<id>\d+)/$', display_event, name='event'),
                       url(r'^search/(?P<page_num>\d+)/', search_event, name='search'),)