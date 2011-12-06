from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

from pixel import tree
tree.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'pixel.views.home', name='home'),
    
    url(r'^upload/$', 'pixel.views.upload',  name='upload'),
    url(r'^upload.ajax$', 'pixel.views.mobileUpload'),
    
    url(r'^detail/(?P<image_id>\d+)$', 'pixel.views.detail', name='detail'),
    url(r'^detail/thumbs/(?P<image_id>\d+)$', 'pixel.views.thumbList', name='thumbList'),
    
    url(r'^d/(?P<short_id>\w+)$', 'pixel.views.short', name='short'),

    url(r'^admin/', include(admin.site.urls)),
    
    
)
