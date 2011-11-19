from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html'}, name='home'),
<<<<<<< HEAD

    url(r'^detail/(?P<id>\d+)$', 'pixel.views.detail', name='detail'),
    url(r'^upload/$', 'pixel.views.upload',  name='upload'),

=======
    url(r'^detail/$', direct_to_template, {'template': 'details.html'}, name='detail'),
    url(r'^loading/$', direct_to_template, {'template': 'loading.html'}, name='loading'),
>>>>>>> afae0e746da28df5ac06a9fa11f6934cd5ccbd14

    url(r'^admin/', include(admin.site.urls)),
    
    
)
