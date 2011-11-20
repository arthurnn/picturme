from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html'}, name='home'),
    
    url(r'^upload/$', 'pixel.views.upload',  name='upload'),
    
    
    url(r'^detail/(?P<image_id>\d+)$', 'pixel.views.detail', name='detail'),
    url(r'^detail/thumbs/(?P<image_id>\d+)$', 'pixel.views.thumbList', name='thumbList'),
    
    

    url(r'^admin/', include(admin.site.urls)),
    
    
)
