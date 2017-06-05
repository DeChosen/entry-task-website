from django.conf.urls import patterns, include, url,static
from django.conf import settings

urlpatterns = patterns('',

    url(r'^test/', include('test_url.urls')),   
#    url(r'^login/', include('login.urls')),
    url(r'^home/', include('events.urls')),
    url(r'^admin/', include('admin.urls')),
    url(r'^', include('login.urls')),
)

if settings.DEBUG:
    urlpatterns += [url(r'^(.*)', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),]
