from django.conf.urls import patterns, url
from views import login_page, redirect_login_page

urlpatterns = [url(r'^$', redirect_login_page),
		url(r'^login/$', login_page, name = 'login')]
