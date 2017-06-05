from django.conf.urls import patterns, url
from .views import test_stuff, test_stuff2

urlpatterns = [url(r'^$', test_stuff),
		url(r'^something/(?P<path>.*)', test_stuff2)]
